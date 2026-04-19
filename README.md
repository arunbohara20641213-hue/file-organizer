# File Organizer

Automatically organize files in your Downloads folder by file type.

## Project Structure

- organizer.py: One-time organizer run.
- watcher.py: Live monitoring mode.
- config.py: File type mappings and shared paths.
- log.txt: Append-only move logs.

## Categories

- PDFs
- Images
- Videos
- Audio
- Code
- Excel
- Word
- Archives
- Others

## Setup

Install the only external dependency:

```bash
pip install watchdog
```

Or install from requirements:

```bash
pip install -r requirements.txt
```

## Run

One-time clean:

```bash
python organizer.py
```

Live watching mode:

```bash
python watcher.py
```

## Notes

- Files are moved from your Downloads root into category subfolders.
- Duplicate names are preserved using suffixes like _copy and _copy2.
- Every successful move is logged to log.txt.
