# Platform Architecture

## Active flow

```text
Manufacturing OLTP
      ↓
Operational extracts
      ↓
Reproducible source snapshots
      ↓
Extract → Clean → Validate
      ↓
Controlled PostgreSQL staging
      ↓
Type 1 dimensions + Machine SCD Type 2
      ↓
Date-aware surrogate-key resolution
      ↓
Idempotent Fact_Production
      ↓
PostgreSQL star schema
      ↓
Semantic analytics view
      ↓
Streamlit / Power BI / SQL analytics
```

## Design principles

1. The warehouse owns table definitions. Pandas does not recreate warehouse schemas.
2. PostgreSQL generates surrogate keys.
3. Facts are loaded at one explicit production-event grain.
4. Machine history is preserved using SCD Type 2.
5. Historical facts resolve the machine version valid on the business date.
6. Production IDs are unique idempotency keys.
7. One source snapshot is processed transactionally.
8. Source and warehouse quality checks fail fast.
9. CI reproduces both ETL runs against PostgreSQL 16.
10. Credentials are provided through environment configuration.
