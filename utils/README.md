# Insight UI Utils

This package provides a simple WebSocket-based system monitoring utility used in the [Insight UI Showcase](https://github.com/alpininsight/insight-ui). It streams live system metrics such as current time, disk usage, and memory consumption to connected WebSocket clients.

## Features

- Sends JSON payload with:
  - Timestamp
  - Disk usage (total, used, free in GB)
  - Memory usage (total, available in GB and percentage)
- Updates every 5 seconds
- Lightweight, no FastAPI or Django dependency
- Built for local testing or developer dashboards
- Built and run with [`uv`](https://github.com/astral-sh/uv)

## Requirements

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv)

## Installation

```bash
uv pip install -e .
```

## Usage

Start the WebSocket server:

```bash
uv run main.py
```

By default, it runs on:

`ws://localhost:8765`

## Example Output

```py
{
  "timestamp": "2025-06-23T10:45:31.812496",
  "disk": {
    "total_gb": 500.11,
    "used_gb": 245.73,
    "free_gb": 254.38
  },
  "memory": {
    "total_gb": 32.0,
    "available_gb": 24.52,
    "percent_used": 23.4
  }
}
```

## License

MIT License © 2025 Alpin Insight AI
