# Contributing to JalDrishti-AI

Thank you for contributing to JalDrishti-AI. This document outlines development standards, Git workflows, and data handling conventions.

## Development Workflow

1. **Branching Model**:
   - `main`: Production-ready, stable codebase. Direct commits to `main` should be reserved for release preparation or project setup.
   - `feature/<feature-name>`: New analytical models, MCDA pillars, or export scripts.
   - `fix/<issue-name>`: Bug fixes and data corrections.
2. **Pull Requests**:
   - Provide a concise summary of changes and validation evidence.
   - Ensure all automated unit tests pass: `pytest tests/`.
   - Never commit sensitive credentials, API keys, or Earth Engine access tokens.

## Git & Large File Storage (Git LFS) Conventions

- Standard Git commits must **never exceed 100 MB**.
- Any dataset larger than 50 MB (such as `maharashtra_village_historical_rainfall_2001_2025_v2.csv`) must be tracked using Git LFS via `.gitattributes`.
- Always verify file size before staging:
  ```bash
  git status
  git lfs status
  ```

## Scientific and Analytical Integrity

- **No Synthetic Data**: Missing or null remote-sensing observations must never be replaced with arbitrary numbers or unverified imputations. Document missing data openly.
- **Accurate Terminology**: The initial slope + rainfall score must always be described as a **preliminary screening proxy**, never as a "validated MCDA model" or "engineering suitability recommendation".
