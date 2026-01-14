# src/api_service/test_db.py
from sqlalchemy import text
from .db.db import engine  # mismo import que ya te está funcionando


def main():
    print("Probando conexión a la base de datos...")
    with engine.connect() as conn:
        # Opción 1: usando text()
        result = conn.execute(text("SELECT 1"))
        print("Resultado SELECT 1:", result.scalar_one())

        # O, alternativamente, podrías usar:
        # result = conn.exec_driver_sql("SELECT 1")
        # print("Resultado SELECT 1:", result.scalar_one())


if __name__ == "__main__":
    main()
