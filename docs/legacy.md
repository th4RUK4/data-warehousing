# Legacy V1

The original implementation by **@th4RUK4** is preserved under `legacy/v1/`.

V1 established the original end-to-end concept:

```text
CSV → staging → dimensions → fact → analytics → Streamlit
```

V2 keeps that manufacturing analytics goal while adding modular ETL, controlled schemas, historical correctness, tests, Docker, CI, secure configuration and a formal collaboration workflow.

The legacy code is preserved for project history and is not used by the active V2 runtime.
