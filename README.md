# ETL Project

A modular ETL (Extract, Transform, Load) pipeline project using Python and Poetry.

## Project Structure

```
etl_project/
├── etl_project/
│   ├── extractors/     # Data extraction modules
│   ├── transformers/   # Data transformation modules
│   ├── loaders/        # Data loading modules
│   ├── config/         # Configuration files
│   ├── utils/          # Utility functions
│   └── pipeline.py     # Main ETL pipeline implementation
├── tests/              # Test files
├── pyproject.toml      # Poetry dependency management
└── README.md          # Project documentation
```

## Setup

1. Install Poetry (package manager):
```bash
pip install poetry
```

2. Install dependencies:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

## Usage

To implement your ETL pipeline:

1. Create specific extractors in `extractors/`
2. Create specific transformers in `transformers/`
3. Create specific loaders in `loaders/`
4. Configure your settings in `config/settings.py`
5. Use the `ETLPipeline` class to run your pipeline

## Development

- Run tests: `poetry run pytest`
- Format code: `poetry run black .`
- Lint code: `poetry run flake8`
- Type checking: `poetry run mypy .`