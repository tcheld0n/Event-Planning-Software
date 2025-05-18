"""
Script simplificado para verificar o PostgreSQL
"""
import os
import subprocess
import platform
import socket
import time

def print_colored(text, color):
    """Imprime texto colorido no terminal."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")

def print_header(title):
    """Imprime um cabeçalho formatado."""
    print("\n" + "=" * 60)
    print_colored(f"  {title}", "blue")
    print("=" * 60)

def print_success(message):
    """Imprime mensagem de sucesso."""
    print_colored(f"✅ {message}", "green")

def print_error(message):
    """Imprime mensagem de erro."""
    print_colored(f"❌ {message}", "red")

def print_info(message):
    """Imprime informação."""
    print(f"ℹ️ {message}")

def is_port_open(host, port, timeout=1):
    """Verifica se a porta está aberta e aceitando conexões."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def is_postgresql_running():
    """Verifica se o PostgreSQL está rodando."""
    # Verifica pelo método mais confiável primeiro: testando a porta
    if is_port_open("localhost", 5432):
        return True
    
    # Método secundário: verificar serviço (Windows)
    if platform.system().lower() == "windows":
        try:
            result = subprocess.run(
                ["sc", "query", "postgresql"], 
                capture_output=True, 
                text=True,
                check=False
            )
            return "RUNNING" in result.stdout
        except Exception:
            pass
    
    # Método terciário: verificar processos (Linux/Mac)
    try:
        if platform.system().lower() == "windows":
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq postgres.exe"], 
                capture_output=True, 
                text=True,
                check=False
            )
            return "postgres.exe" in result.stdout
        else:
            result = subprocess.run(
                ["ps", "aux"], 
                capture_output=True, 
                text=True,
                check=False
            )
            return "postgres" in result.stdout
    except Exception:
        pass
    
    return False

def test_database_connection():
    """Testa a conexão com o banco de dados PostgreSQL."""
    try:
        # Tentar importar psycopg2
        try:
            import psycopg2
        except ImportError:
            print_error("Módulo psycopg2 não encontrado")
            print_info("Instalando psycopg2-binary...")
            subprocess.run(["pip", "install", "psycopg2-binary"], check=True)
            import psycopg2
        
        print_info("Testando conexão com PostgreSQL...")
        
        # Tenta conectar ao banco de dados
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="123456",
            database="postgres",
            connect_timeout=3
        )
        
        # Executa uma consulta simples
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        # Fecha conexão
        cursor.close()
        conn.close()
        
        print_success(f"Conexão bem-sucedida! Versão: {version[0]}")
        return True
    except Exception as e:
        print_error(f"Erro ao conectar ao banco: {str(e)}")
        return False

def main():
    """Função principal."""
    print_header("VERIFICAÇÃO DO POSTGRESQL")
    
    # Verifica se o PostgreSQL está rodando
    print_info("Verificando se o PostgreSQL está rodando...")
    
    if is_postgresql_running():
        print_success("PostgreSQL está em execução!")
        
        # Testa conexão com o banco
        if test_database_connection():
            print_header("TUDO PRONTO!")
            print("O PostgreSQL está configurado e pronto para uso.")
            print("Execute o aplicativo com: python main.py")
            return True
        else:
            print_header("CONEXÃO FALHOU")
            print("O serviço PostgreSQL está rodando, mas a conexão falhou.")
            print("\nPossíveis causas:")
            print("1. A senha do usuário 'postgres' não é '123456'")
            print("2. O banco 'postgres' não existe ou está inacessível")
            print("3. Configurações de acesso restritivas (pg_hba.conf)")
            
            print("\nSoluções:")
            print("1. Redefinir senha: ALTER USER postgres WITH PASSWORD '123456';")
            print("2. Verifique as configurações em:")
            print("   C:\\Program Files\\PostgreSQL\\[versão]\\data\\pg_hba.conf")
    else:
        print_error("PostgreSQL não está rodando")
        
        print_header("COMO RESOLVER")
        print("1. Verifique se o PostgreSQL está instalado")
        print("2. Inicie o serviço PostgreSQL")
        print("   - Abra 'services.msc' (Executar -> services.msc)")
        print("   - Encontre 'PostgreSQL'")
        print("   - Clique com botão direito -> 'Iniciar'")
        
        print("\nSe não estiver instalado:")
        print("1. Baixe em: https://www.postgresql.org/download/windows/")
        print("2. Execute o instalador e siga as instruções")
        print("3. Use senha: 123456")
        print("4. Use porta padrão: 5432")
    
    return False

if __name__ == "__main__":
    main()
