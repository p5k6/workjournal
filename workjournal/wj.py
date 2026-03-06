#!/usr/bin/env python3
"""wj - workjournal CLI tool"""

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"

# Project root is one level above this package directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_PATH = os.path.expanduser("~/.config/wj/config.json")
DEFAULT_AUDIO_DEVICE = "0"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH) as f:
        return json.load(f)


def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")


def get_audio_device(args):
    """Resolve audio device following precedence: flag > env var > config > default."""
    if getattr(args, "audio_device", None) is not None:
        return str(args.audio_device)
    if "WJ_AUDIO_DEVICE" in os.environ:
        return os.environ["WJ_AUDIO_DEVICE"]
    config = load_config()
    if "audio_device" in config:
        return str(config["audio_device"])
    return DEFAULT_AUDIO_DEVICE


def load_prompt(name):
    path = os.path.join(PROJECT_ROOT, "prompts-runtime", name)
    with open(path) as f:
        return f.read().strip()


def get_log_path():
    today = datetime.date.today()
    return os.path.expanduser(f"~/worklog/{today.year}/{today.strftime('%Y-%m-%d')}.md")


def ensure_log_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def check_ollama():
    """Check Ollama is reachable and the model is available. Exit with a clear message if not."""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        r.raise_for_status()
    except requests.exceptions.ConnectionError:
        print(
            f"Error: Ollama does not appear to be running at {OLLAMA_URL}.\n"
            "Start it with: ollama serve   or   brew services start ollama",
            file=sys.stderr,
        )
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not reach Ollama: {e}", file=sys.stderr)
        sys.exit(1)

    available = [m["name"] for m in r.json().get("models", [])]
    # Match on model name prefix so "qwen2.5:7b" matches "qwen2.5:7b" or tagged variants
    if not any(m == OLLAMA_MODEL or m.startswith(OLLAMA_MODEL) for m in available):
        print(
            f"Error: Model '{OLLAMA_MODEL}' is not available in Ollama.\n"
            f"Pull it with: ollama pull {OLLAMA_MODEL}",
            file=sys.stderr,
        )
        sys.exit(1)


def cleanup_with_ollama(text):
    prompt = load_prompt("cleanup.md")
    full_prompt = f"{prompt}\n\nNotes:\n{text}"
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": full_prompt, "stream": False},
            timeout=60,
        )
        r.raise_for_status()
        return r.json()["response"].strip()
    except requests.exceptions.ConnectionError:
        print(
            f"Error: Ollama is not reachable at {OLLAMA_URL}.\n"
            "Start it with: ollama serve   or   brew services start ollama",
            file=sys.stderr,
        )
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: Ollama request timed out. The model may be loading — try again.", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: Ollama request failed: {e}", file=sys.stderr)
        sys.exit(1)


def build_entry(body):
    time = datetime.datetime.now().strftime("%H:%M")
    return f"## {time}\n\n{body}\n"


def edit_in_editor(text):
    editor = os.environ.get("EDITOR", "vim")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(text)
        tmp = f.name
    subprocess.run([editor, tmp])
    with open(tmp) as f:
        result = f.read()
    os.unlink(tmp)
    return result


def preview_and_confirm(entry):
    """Show entry preview and ask what to do. Returns (action, entry)."""
    print("\n--- Preview ---")
    print(entry)
    print("---------------")
    while True:
        choice = input("[a]ppend / [e]dit / [d]iscard: ").strip().lower()
        if choice in ("a", "append", ""):
            return "append", entry
        elif choice in ("e", "edit"):
            edited = edit_in_editor(entry)
            return "append", edited
        elif choice in ("d", "discard"):
            return "discard", entry
        print("Please enter a, e, or d.")


def append_to_log(entry):
    path = get_log_path()
    ensure_log_dir(path)
    today = datetime.date.today().strftime("%Y-%m-%d")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(f"# {today}\n\n")
    with open(path, "a") as f:
        f.write(entry + "\n")
    print(f"Appended to {path}")


def record_audio(filepath, device=DEFAULT_AUDIO_DEVICE):
    try:
        proc = subprocess.Popen(
            [
                "ffmpeg",
                "-f", "avfoundation",
                "-i", f":{device}",  # macOS audio input device
                "-ar", "16000",      # 16 kHz sample rate
                "-ac", "1",          # mono
                "-y",                # overwrite output without prompting
                filepath,
            ],
            stdin=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        print("Error: 'ffmpeg' not found. Install it: brew install ffmpeg", file=sys.stderr)
        sys.exit(1)
    print(f"Recording... Press Enter to stop. (device :{device})")
    try:
        input()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            proc.stdin.write(b"q\n")
            proc.stdin.flush()
        except Exception:
            pass
        proc.wait()


def transcribe(audio_path, output_dir):
    try:
        result = subprocess.run(
            [
                "whisper",
                audio_path,
                "--model", "base",
                "--output_format", "txt",
                "--output_dir", output_dir,
                "--fp16", "False",
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
    except FileNotFoundError:
        print(
            "Error: 'whisper' not found. Install: pip install openai-whisper",
            file=sys.stderr,
        )
        sys.exit(1)

    base = os.path.splitext(os.path.basename(audio_path))[0]
    txt_path = os.path.join(output_dir, base + ".txt")
    if not os.path.exists(txt_path):
        print("Error: Transcription failed.", file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(1)

    with open(txt_path) as f:
        return f.read().strip()


def cmd_log(args):
    if not args.transcript_only:
        check_ollama()

    device = get_audio_device(args)

    audio_save_path = None
    if args.keep_audio:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_save_path = f"/tmp/wj_audio_{ts}.wav"

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "recording.wav")
        record_audio(audio_path, device)
        print("Transcribing...")
        text = transcribe(audio_path, tmpdir)
        if audio_save_path:
            shutil.copy2(audio_path, audio_save_path)

    if args.transcript_only:
        print("\n--- Raw transcript ---")
        print(text if text else "(empty — Whisper produced no output)")
        print("----------------------")
        if audio_save_path:
            print(f"Audio saved to: {audio_save_path}")
        return

    if not text:
        print("No speech detected.", file=sys.stderr)
        sys.exit(1)
    print(f"Transcript: {text}")
    if audio_save_path:
        print(f"Audio saved to: {audio_save_path}")
    print("Cleaning up with Ollama...")
    body = cleanup_with_ollama(text)
    entry = build_entry(body)
    action, final_entry = preview_and_confirm(entry)
    if action == "append":
        append_to_log(final_entry)


def cmd_paste(args):
    check_ollama()
    if not sys.stdin.isatty():
        text = sys.stdin.read().strip()
    else:
        print("Enter your notes (Ctrl+D when done):")
        lines = []
        try:
            while True:
                lines.append(input())
        except EOFError:
            text = "\n".join(lines).strip()

    if not text:
        print("No input provided.", file=sys.stderr)
        sys.exit(1)

    print("Cleaning up with Ollama...")
    body = cleanup_with_ollama(text)
    entry = build_entry(body)

    if args.dry_run:
        print("\n--- Dry run (not appended) ---")
        print(entry)
        print("------------------------------")
        return

    action, final_entry = preview_and_confirm(entry)
    if action == "append":
        append_to_log(final_entry)


def cmd_config(args):
    config = load_config()
    if args.config_command == "get":
        key = args.key
        if key in config:
            print(f"{key} = {config[key]}")
        else:
            print(f"{key} is not set (default: {DEFAULT_AUDIO_DEVICE if key == 'audio_device' else 'none'})")
    elif args.config_command == "set":
        config[args.key] = args.value
        save_config(config)
        print(f"Set {args.key} = {args.value}  (saved to {CONFIG_PATH})")
    else:
        # No subcommand: show all config
        if config:
            for k, v in config.items():
                print(f"{k} = {v}")
        else:
            print(f"No config set. ({CONFIG_PATH})")


def cmd_today(args):
    path = get_log_path()
    if not os.path.exists(path):
        print(f"No log for today. ({path})")
        return
    with open(path) as f:
        print(f.read(), end="")


def cmd_edit(args):
    path = get_log_path()
    ensure_log_dir(path)
    if not os.path.exists(path):
        today = datetime.date.today().strftime("%Y-%m-%d")
        with open(path, "w") as f:
            f.write(f"# {today}\n\n")
    editor = os.environ.get("EDITOR", "vim")
    subprocess.run([editor, path])


def main():
    parser = argparse.ArgumentParser(prog="wj", description="Work journal CLI")
    sub = parser.add_subparsers(dest="command")
    log_parser = sub.add_parser("log", help="Record a voice note and append to journal")
    log_parser.add_argument("--transcript-only", action="store_true", help="Record and transcribe only; do not call Ollama or append")
    log_parser.add_argument("--keep-audio", action="store_true", help="Save recorded audio to /tmp for debugging")
    log_parser.add_argument("--audio-device", metavar="N", help="FFmpeg AVFoundation audio device index (overrides config and env)")
    paste_parser = sub.add_parser("paste", help="Paste or type notes and append to journal")
    paste_parser.add_argument("--dry-run", action="store_true", help="Show generated entry without appending to journal")
    sub.add_parser("today", help="Print today's log")
    sub.add_parser("edit", help="Open today's log in editor")
    config_parser = sub.add_parser("config", help="Get or set persistent configuration")
    config_sub = config_parser.add_subparsers(dest="config_command")
    get_parser = config_sub.add_parser("get", help="Get a config value")
    get_parser.add_argument("key", help="Config key (e.g. audio_device)")
    set_parser = config_sub.add_parser("set", help="Set a config value")
    set_parser.add_argument("key", help="Config key (e.g. audio_device)")
    set_parser.add_argument("value", help="Value to set")
    args = parser.parse_args()

    if args.command == "log":
        cmd_log(args)
    elif args.command == "paste":
        cmd_paste(args)
    elif args.command == "today":
        cmd_today(args)
    elif args.command == "edit":
        cmd_edit(args)
    elif args.command == "config":
        cmd_config(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
