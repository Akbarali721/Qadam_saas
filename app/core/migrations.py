from sqlalchemy import Engine, text


def run_platform_startup_migrations(engine: Engine) -> None:
    if engine.dialect.name != "sqlite":
        return

    with engine.begin() as connection:
        product_columns = connection.execute(text("PRAGMA table_info(products)")).mappings().all()
        product_column_names = {column["name"] for column in product_columns}
        if "title" not in product_column_names:
            connection.execute(
                text("ALTER TABLE products ADD COLUMN title VARCHAR(120) NOT NULL DEFAULT ''"),
            )
        if "status" not in product_column_names:
            connection.execute(
                text("ALTER TABLE products ADD COLUMN status VARCHAR(32) NOT NULL DEFAULT 'draft'"),
            )
        connection.execute(text("UPDATE products SET title = name WHERE title = ''"))
        connection.execute(
            text(
                "UPDATE products SET status = CASE "
                "WHEN is_active = 1 THEN 'active' "
                "ELSE 'planned' END WHERE status = 'draft'",
            ),
        )
