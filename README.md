# Resume Analyzer CLI

A Python CLI tool to analyze PDF resumes, count key skill mentions, and suggest improvements based on missing keywords.

## Features

- **Extracts text** from a PDF resume using PyMuPDF
- **Counts occurrences** of defined skill keywords
- **Suggests improvements** for missing or underrepresented skill categories
- Supports **custom skill databases** via JSON

## Requirements

- Python 3.7+
- [PyMuPDF](https://pypi.org/project/PyMuPDF/)

Install dependencies:
```bash
pip install PyMuPDF
