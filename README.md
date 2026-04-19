# File Organizer

Automatically organize files in your Downloads folder by file type, with undo, reporting, and custom rules support.

## Project Structure

- organizer.py: Core organization logic with transaction logging.
- watcher.py: Live monitoring mode with event debouncing.
- config.py: File type mappings, keyword/exact rules, and shared paths.
- undo.py: Revert recent file moves.
- report.py: Generate summary statistics.
- log.txt: Human-readable activity log.
- transactions.jsonl: Structured transaction log (for undo/report).

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

## Usage

### One-time Organization

```bash
python organizer.py
```

### Live Watching Mode

```bash
python watcher.py
```

Press Ctrl+C to stop watching.

### Undo Recent Moves

Revert the last move:
```bash
python undo.py
```

Revert the last 5 moves:
```bash
python undo.py --count 5
```

### View Summary Report

Show all-time statistics:
```bash
python report.py
```

Show today's activity:
```bash
python report.py --date today
```

Show activity from yesterday:
```bash
python report.py --date yesterday
```

Show activity from past week:
```bash
python report.py --date week
```

Show activity for a specific date:
```bash
python report.py --date 2026-04-19
```

## Features

- **Automatic categorization** by file extension.
- **Duplicate-safe moves** with automatic suffix generation (_copy, _copy2, etc).
- **Transaction logging** for complete audit trail and undo capability.
- **Event debouncing** to handle burst downloads efficiently.
- **Hidden/system/temp file skipping** on Windows.
- **Keyword-based rules** for intelligent file routing.

## Configuration

Edit `config.py` to customize behavior:

### Keyword Rules

Match filenames against patterns to override extension-based categorization:

```python
KEYWORD_RULES = [
    {"pattern": "invoice", "target": "Invoices", "case_sensitive": False},
    {"pattern": "receipt", "target": "Receipts", "case_sensitive": False},
    {"pattern": "tax2026", "target": "Tax-2026", "case_sensitive": False},
]
```

### Exact Rules

Match exact filenames:

```python
EXACT_RULES = {
    "manifest.json": "Config",
    "settings.ini": "Config",
}
```

### Skip Patterns

Files matching these patterns are automatically skipped:

```python
IGNORED_FILE_NAMES = {"desktop.ini", "thumbs.db"}
TEMP_EXTENSIONS = {".tmp", ".part", ".crdownload", ".download"}
```

### Debounce Window

Adjust watcher responsiveness (seconds to wait after last file event before organizing):

```python
DEBOUNCE_SECONDS = 2.0
```

## Notes

- Files are moved from your Downloads root into category subfolders.
- Every successful move is logged to both log.txt and transactions.jsonl.
- Undo is best-effort and requires source/destination paths to be accessible.
- Keyword rules are checked before extension rules for flexibility.

