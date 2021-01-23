import sqlalchemy

metadata = sqlalchemy.MetaData()

dishes = sqlalchemy.Table(
    "dishes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("device_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(length=30), nullable=False),
    sqlalchemy.Column("ingredients", sqlalchemy.String(length=150), nullable=False),
    sqlalchemy.Column("quantity", sqlalchemy.Float, nullable=False),
)

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(length=30), nullable=False),
)

devices = sqlalchemy.Table(
    "devices",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False),
)
