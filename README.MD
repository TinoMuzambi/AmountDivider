# Amount Divider

A small Flask application that splits an amount into decreasing partitions while preserving the original total. It is useful for prize pools, allocations, and other weighted distributions.

## Run locally

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
flask --app app run --debug
```

Open `http://127.0.0.1:5000` and enter a positive amount and between 1 and 1,000 partitions.

## Test

```bash
pytest
```

## Deploy

The included `Procfile` starts the application with Gunicorn:

```bash
gunicorn app:app
```

Set the platform runtime to Python 3.12 or another currently supported Python 3 release.
