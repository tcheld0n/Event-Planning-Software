import psycopg2
from psycopg2 import sql

# Dados de acesso
HOST = "localhost"
USER = "postgres"
PASSWORD = "123456"
DB_NAME = "postgres"

def reset_database():
    # Conecta ao banco postgres (serve como fallback caso nosso banco seja apagado)
    conn = psycopg2.connect(host=HOST, user=USER, password=PASSWORD, dbname="postgres")
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("Encerrando conexões ativas...")
    try:
        # Encerra todas as conexões existentes ao banco
        cursor.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity 
            WHERE pg_stat_activity.datname = '{DB_NAME}'
            AND pid <> pg_backend_pid()
        """)
    except Exception as e:
        print(f"Aviso ao encerrar conexões: {e}")
    
    # Verifica se o banco existe
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
    exists = cursor.fetchone()
    
    if exists:
        print(f"Removendo banco de dados '{DB_NAME}'...")
        try:
            cursor.execute(f"DROP DATABASE {DB_NAME}")
            print(f"Banco de dados '{DB_NAME}' removido com sucesso!")
        except Exception as e:
            print(f"Erro ao remover banco: {e}")
    else:
        print(f"Banco de dados '{DB_NAME}' não existe ou já foi removido.")
    
    print("Banco será recriado automaticamente ao iniciar a aplicação.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("=== RESET COMPLETO DO BANCO DE DADOS ===")
    reset_database()
    print("Concluído!")