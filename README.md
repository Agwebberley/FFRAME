# FFRAME
Goal: Features of FRAME using Flask

Folder Structure:
```bash
/flask-graphql-erp/
│
├── /app/
│   ├── __init__.py          # App factory
│   ├── /models/            # SQLAlchemy models
│   │   └── user.py
│   ├── /schemas/           # Graphene schemas
│   │   └── user_schema.py
│   ├── /services/          # Business logic
│   │   └── user_service.py
│   ├── /graphql/           # GraphQL schema and setup
│   │   └── schema.py
│   └── /extensions/        # DB, Migrations, etc.
│       └── __init__.py
│
├── /migrations/           # Alembic migrations
├── config.py              # Configurations
├── run.py                 # Entry point
└── requirements.txt
```
