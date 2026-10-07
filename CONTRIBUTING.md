# Contributing

This repository is maintained jointly by **@th4RUK4** and **@akindaG**.

## Branch workflow

Do not develop substantial features directly on `main`.

Use branches such as:

- `feature/akinda-<topic>`
- `feature/tharuka-<topic>`
- `fix/<topic>`
- `docs/<topic>`
- `refactor/<topic>`

Open a pull request into `main`, allow CI to run, and request review from the other collaborator.

## Local validation

```bash
pip install -r requirements.txt
python -m pytest
```

For the full local platform:

```bash
docker compose up --build
```

The Streamlit dashboard is available at `http://localhost:8501`.

## Commit style

Prefer focused commits:

```text
feat: add machine quality KPI
fix: preserve historical SCD lookup
test: cover invalid production references
refactor: split fact loading from orchestration
docs: document warehouse grain
ci: strengthen integration validation
```

Review for correctness first: grain, surrogate-key resolution, historical validity, idempotency, data quality, reproducibility and credential safety.
