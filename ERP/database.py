import sqlite3

DB_NAME = "erp.db"

def get_connection():
    """Retorna uma conexão com o banco de dados SQLite com foreign keys ativadas."""
    conn = sqlite3.connect(DB_NAME)
    # Permite aceder às colunas pelo nome (ex: row['razao_social'])
    conn.row_factory = sqlite3.Row
    # Garante a integridade referencial no SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn