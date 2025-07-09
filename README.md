# PubMed Fetcher

Command-line tool to fetch PubMed research papers with at least one non-academic (company-affiliated) author.

## Features

- Full PubMed query support
- Detects pharmaceutical/biotech affiliations
- Saves output to CSV or prints to console
- Typed Python with Pydantic
- Poetry-based setup

## Installation

```bash
poetry install
```

## Usage

```bash
poetry run get-papers-list "cancer treatment" --file results.csv --debug
```