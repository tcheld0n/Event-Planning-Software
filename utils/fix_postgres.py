"""
Script de diagnóstico e recuperação do PostgreSQL
Este script ajuda a resolver problemas de conexão com o banco PostgreSQL,
especialmente o erro 'Connection refused: getsockopt'
"""
import os
import sys
import time
import subprocess
import platform
import socket
import ctypes

def is_admin():
    """Verifica se o script está sendo executado como administrador."""
    try:
        if platform.system().lower() == "windows":
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except:
        return False

def print_colored(text, color):
    """Imprime texto colorido."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")

def print_header(message):
    """Imprime um cabeçalho formatado."""
    print("\n" + "=" * 70)
    print_colored(f"  {message}", "blue")
    print("=" * 70)

def print_success(message):
    """Imprime mensagem de sucesso."""
    print_colored(f"✅ {message}", "green")

def print_error(message):
    """Imprime mensagem de erro."""
    print_colored(f"❌ {message}", "red")

def print_warning(message):
    """Imprime aviso."""
    print_colored(f"⚠️ {message}", "yellow")

def print_info(message):
    """Imprime informação."""
    print(f"ℹ️ {message}")

def is_port_open(host, port):
    """Verifica se a porta está aberta e aceitando conexões."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def get_postgresql_status():
    """Obtém informações detalhadas sobre o status do PostgreSQL."""
    status = {
        "installed": False,
        "running": False,
        "port_open": False,
        "version": None,
        "data_dir": None,
        "config_file": None
    }
    
    # Verifica instalação
    try:
        if platform.system().lower() == "windows":
            # Verifica no registro do Windows
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\PostgreSQL")
                status["installed"] = True
            except:
                # Procura por instalações típicas
                paths_to_check = [
                    r"C:\Program Files\PostgreSQL",
                    r"C:\Program Files (x86)\PostgreSQL"
                ]
                for path in paths_to_check:
                    if os.path.exists(path):
                        status["installed"] = True
                        break
        else:
            # Linux/Mac
            result = subprocess.run(
                ["which", "psql"], 
                capture_output=True, 
                text=True
            )
            status["installed"] = result.returncode == 0
    except Exception as e:
        print_warning(f"Erro ao verificar instalação: {e}")
    
    # Verifica se está em execução
    try:
        if platform.system().lower() == "windows":
            result = subprocess.run(
                ["sc", "query", "postgresql"], 
                capture_output=True, 
                text=True
            )
            status["running"] = "RUNNING" in result.stdout
        else:
            result = subprocess.run(
                ["ps", "aux"], 
                capture_output=True, 
                text=True
            )
            status["running"] = "postgres" in result.stdout
    except Exception as e:
        print_warning(f"Erro ao verificar execução: {e}")
    
    # Verifica porta
    status["port_open"] = is_port_open("localhost", 5432)
    
    # Tenta obter versão
    try:
        if platform.system().lower() == "windows":
            pg_paths = []
            if os.path.exists(r"C:\Program Files\PostgreSQL"):
                for dir in os.listdir(r"C:\Program Files\PostgreSQL"):
                    if os.path.isdir(os.path.join(r"C:\Program Files\PostgreSQL", dir)):
                        pg_paths.append(os.path.join(r"C:\Program Files\PostgreSQL", dir))
            
            if pg_paths:
                newest_version = sorted(pg_paths)[-1]
                status["version"] = os.path.basename(newest_version)
                status["data_dir"] = os.path.join(newest_version, "data")
                status["config_file"] = os.path.join(status["data_dir"], "postgresql.conf")
        else:
            # Linux/Mac
            result = subprocess.run(
                ["psql", "--version"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                status["version"] = result.stdout.strip().split(" ")[-1]
    except Exception as e:
        print_warning(f"Erro ao obter versão: {e}")
    
    return status

def start_postgresql():
    """Tenta iniciar o PostgreSQL."""
    if platform.system().lower() == "windows":
        print_info("Tentando iniciar o serviço PostgreSQL...")
        if is_admin():
            try:
                subprocess.run(
                    ["net", "start", "postgresql"],
                    capture_output=True,
                    text=True
                )
                time.sleep(5)  # Dá tempo para o serviço iniciar
                return get_postgresql_status()["running"]
            except Exception as e:
                print_error(f"Erro ao iniciar PostgreSQL: {e}")
                return False
        else:
            print_warning("Você precisa de privilégios de administrador para iniciar o serviço")
            print_info("Execute este script como administrador (botão direito -> Executar como administrador)")
            return False
    else:
        # Linux/Mac
        print_info("Tentando iniciar o serviço PostgreSQL...")
        if is_admin():
            try:
                subprocess.run(
                    ["systemctl", "start", "postgresql"],
                    capture_output=True,
                    text=True
                )
                time.sleep(5)  # Dá tempo para o serviço iniciar
                return get_postgresql_status()["running"]
            except Exception as e:
                print_error(f"Erro ao iniciar PostgreSQL: {e}")
                return False
        else:
            print_warning("Você precisa de privilégios de administrador para iniciar o serviço")
            print_info("Execute este script com sudo")
            return False

def test_database_connection():
    """Testa a conexão com o banco de dados."""
    try:
        import psycopg2
        
        print_info("Testando conexão com o banco de dados...")
        
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="123456",
            database="postgres",
            connect_timeout=5
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        print_success(f"Conexão ao banco de dados bem-sucedida!")
        print_info(f"Versão do PostgreSQL: {version[0]}")
        return True
    except ImportError:
        print_error("O módulo psycopg2 não está instalado.")
        print_info("Instale-o com: pip install psycopg2-binary")
        return False
    except Exception as e:
        print_error(f"Erro ao conectar ao banco de dados: {e}")
        return False

def find_postgresql_files():
    """Tenta encontrar arquivos importantes do PostgreSQL."""
    files = {
        "binaries": [],
        "data_dir": None,
        "config_file": None,
        "log_file": None
    }
    
    if platform.system().lower() == "windows":
        # Locais típicos de instalação no Windows
        pg_dirs = []
        
        # Program Files
        if os.path.exists(r"C:\Program Files\PostgreSQL"):
            for dir in os.listdir(r"C:\Program Files\PostgreSQL"):
                full_path = os.path.join(r"C:\Program Files\PostgreSQL", dir)
                if os.path.isdir(full_path):
                    pg_dirs.append(full_path)
        
        # Program Files (x86)
        if os.path.exists(r"C:\Program Files (x86)\PostgreSQL"):
            for dir in os.listdir(r"C:\Program Files (x86)\PostgreSQL"):
                full_path = os.path.join(r"C:\Program Files (x86)\PostgreSQL", dir)
                if os.path.isdir(full_path):
                    pg_dirs.append(full_path)
        
        # Procura pelos binários
        for pg_dir in pg_dirs:
            bin_dir = os.path.join(pg_dir, "bin")
            if os.path.exists(bin_dir):
                files["binaries"].append(bin_dir)
            
            # Procura pelo diretório de dados
            data_dir = os.path.join(pg_dir, "data")
            if os.path.exists(data_dir):
                files["data_dir"] = data_dir
                
                # Procura pelo arquivo de configuração
                config_file = os.path.join(data_dir, "postgresql.conf")
                if os.path.exists(config_file):
                    files["config_file"] = config_file
                
                # Procura pelos logs
                log_dir = os.path.join(data_dir, "log")
                if os.path.exists(log_dir):
                    # Pega o arquivo de log mais recente
                    logs = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith(".log")]
                    if logs:
                        files["log_file"] = sorted(logs, key=os.path.getmtime, reverse=True)[0]
    else:
        # Linux/Mac
        try:
            # Procura pelos binários
            result = subprocess.run(
                ["which", "psql"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                files["binaries"].append(os.path.dirname(result.stdout.strip()))
            
            # Procura pelo diretório de dados (Linux)
            data_dirs = [
                "/var/lib/postgresql/data",
                "/var/lib/pgsql/data",
                "/usr/local/pgsql/data"
            ]
            
            for dir in data_dirs:
                if os.path.exists(dir):
                    files["data_dir"] = dir
                    break
            
            # Procura pelo arquivo de configuração
            if files["data_dir"]:
                config_file = os.path.join(files["data_dir"], "postgresql.conf")
                if os.path.exists(config_file):
                    files["config_file"] = config_file
            
            # Procura pelo log
            log_dirs = [
                "/var/log/postgresql",
                "/var/log/pgsql"
            ]
            
            for dir in log_dirs:
                if os.path.exists(dir):
                    logs = [os.path.join(dir, f) for f in os.listdir(dir) if "postgresql" in f.lower()]
                    if logs:
                        files["log_file"] = sorted(logs, key=os.path.getmtime, reverse=True)[0]
                    break
        except Exception as e:
            print_warning(f"Erro ao procurar arquivos do PostgreSQL: {e}")
    
    return files

def check_network_settings():
    """Verifica e mostra configurações de rede."""
    print_header("CONFIGURAÇÕES DE REDE")
    
    # Verifica porta 5432
    if is_port_open("localhost", 5432):
        print_success("Porta 5432 está aberta e aceitando conexões")
    else:
        print_error("Porta 5432 não está acessível")
        
        # Verifica se algum outro processo está usando a porta
        try:
            if platform.system().lower() == "windows":
                result = subprocess.run(
                    ["netstat", "-ano"], 
                    capture_output=True, 
                    text=True
                )
                for line in result.stdout.split("\n"):
                    if ":5432" in line:
                        print_warning(f"Processo usando a porta 5432: {line}")
            else:
                result = subprocess.run(
                    ["lsof", "-i", ":5432"], 
                    capture_output=True, 
                    text=True
                )
                if result.stdout.strip():
                    print_warning(f"Processo usando a porta 5432:\n{result.stdout}")
        except Exception as e:
            print_warning(f"Erro ao verificar processos na porta 5432: {e}")
    
    # Verifica binding no arquivo de configuração
    pg_status = get_postgresql_status()
    if pg_status["config_file"] and os.path.exists(pg_status["config_file"]):
        try:
            with open(pg_status["config_file"], "r") as f:
                config = f.read()
                
            # Verifica listen_addresses
            import re
            match = re.search(r"listen_addresses\s*=\s*'([^']*)'", config)
            if match:
                listen_addresses = match.group(1)
                print_info(f"listen_addresses no postgresql.conf: '{listen_addresses}'")
                
                if listen_addresses == "localhost" or listen_addresses == "127.0.0.1":
                    print_info("O PostgreSQL está configurado para aceitar apenas conexões locais")
                elif listen_addresses == "*":
                    print_info("O PostgreSQL está configurado para aceitar conexões de qualquer endereço")
                else:
                    print_info(f"O PostgreSQL está configurado para aceitar conexões apenas de: {listen_addresses}")
            else:
                print_warning("Não foi possível encontrar a configuração listen_addresses")
        except Exception as e:
            print_warning(f"Erro ao ler arquivo de configuração: {e}")

def fix_postgresql_problems():
    """Tenta corrigir problemas comuns do PostgreSQL."""
    print_header("TENTANDO CORRIGIR PROBLEMAS")
    
    pg_status = get_postgresql_status()
    pg_files = find_postgresql_files()
    
    # Se não estiver instalado, não podemos fazer nada
    if not pg_status["installed"]:
        print_error("PostgreSQL não parece estar instalado")
        print_info("Por favor, instale o PostgreSQL primeiro")
        return False
    
    # Se não estiver rodando, tenta iniciar
    if not pg_status["running"]:
        print_warning("PostgreSQL não está em execução")
        
        # Tenta iniciar o serviço
        print_info("Tentando iniciar o serviço PostgreSQL...")
        if start_postgresql():
            print_success("PostgreSQL iniciado com sucesso!")
        else:
            print_error("Não foi possível iniciar o PostgreSQL automaticamente")
            
            # Verifica logs para problemas
            if pg_files["log_file"] and os.path.exists(pg_files["log_file"]):
                print_info("Verificando logs para possíveis erros...")
                try:
                    with open(pg_files["log_file"], "r") as f:
                        log_content = f.read()
                        
                    # Procura por erros comuns
                    error_patterns = [
                        "FATAL:",
                        "ERROR:",
                        "could not bind",
                        "permission denied",
                        "already in use",
                        "failed to start"
                    ]
                    
                    for line in log_content.split("\n"):
                        if any(pattern in line for pattern in error_patterns):
                            print_warning(f"Erro encontrado no log: {line}")
                except Exception as e:
                    print_warning(f"Erro ao ler arquivo de log: {e}")
    
    # Se a porta não estiver aberta
    if not pg_status["port_open"] and pg_status["running"]:
        print_warning("PostgreSQL parece estar rodando, mas a porta 5432 não está acessível")
        check_network_settings()
    
    # Tenta conexão final
    if test_database_connection():
        return True
    
    # Se chegamos aqui, não conseguimos resolver o problema automaticamente
    print_warning("Não foi possível resolver o problema automaticamente")
    print_info("Veja as recomendações a seguir para resolver manualmente")
    return False

def show_manual_solutions():
    """Mostra soluções manuais para problemas comuns."""
    print_header("SOLUÇÕES MANUAIS")
    
    print("1. Verifique se o PostgreSQL está instalado corretamente")
    print("   - O instalador pode ser encontrado em: https://www.postgresql.org/download/")
    
    print("\n2. Verifique se o serviço PostgreSQL está em execução")
    if platform.system().lower() == "windows":
        print("   - Abra o Painel de Controle -> Ferramentas Administrativas -> Serviços")
        print("   - Procure por 'PostgreSQL' e verifique se está em execução")
        print("   - Se não estiver, clique com o botão direito e selecione 'Iniciar'")
    else:
        print("   - Execute: sudo systemctl status postgresql")
        print("   - Se não estiver em execução, execute: sudo systemctl start postgresql")
    
    print("\n3. Verifique as configurações de rede do PostgreSQL")
    print("   - Abra o arquivo postgresql.conf (geralmente em [instalação]/data/)")
    print("   - Verifique a configuração listen_addresses")
    print("   - Deve ser '*' ou incluir 'localhost'")
    
    print("\n4. Verifique o arquivo pg_hba.conf para permissões de conexão")
    print("   - Deve haver uma linha permitindo conexões locais, como:")
    print("   - host all all 127.0.0.1/32 md5")
    
    print("\n5. Verifique se a senha está correta")
    if platform.system().lower() == "windows":
        print("   - Abra o SQL Shell (psql) do menu Iniciar")
        print("   - Quando solicitado, use senha: 123456")
        print("   - Se não funcionar, redefina a senha:")
        print("   - Execute: ALTER USER postgres WITH PASSWORD '123456';")
    else:
        print("   - Execute: sudo -u postgres psql")
        print("   - Digite: ALTER USER postgres WITH PASSWORD '123456';")
        print("   - Digite: \\q para sair")
    
    print("\n6. Reinicie o computador")
    print("   - Às vezes, reiniciar o computador resolve problemas de conexão")

def create_utils_dir():
    """Cria diretório utils se não existir."""
    if not os.path.exists(""):
        try:
            os.makedirs("")
            print_success("Diretório 'utils' criado com sucesso")
        except Exception as e:
            print_error(f"Erro ao criar diretório 'utils': {e}")

def show_installation_instructions():
    """Mostra instruções de instalação do PostgreSQL."""
    print_header("INSTALAÇÃO DO POSTGRESQL")
    
    if platform.system().lower() == "windows":
        print("1. Baixe o instalador do PostgreSQL para Windows:")
        print("   https://www.enterprisedb.com/downloads/postgres-postgresql-downloads")
        
        print("\n2. Execute o instalador e siga as instruções:")
        print("   - Selecione todos os componentes (PostgreSQL Server, pgAdmin, etc.)")
        print("   - Use o diretório de instalação padrão")
        print("   - Use a senha: 123456")
        print("   - Use a porta padrão: 5432")
        print("   - Use a configuração regional padrão")
        
        print("\n3. Após a instalação, o PostgreSQL deve iniciar automaticamente")
        print("   Se não iniciar, abra o Painel de Controle -> Ferramentas Administrativas -> Serviços")
        print("   Procure por 'PostgreSQL' e inicie o serviço")
    else:
        print("Para Ubuntu/Debian:")
        print("   sudo apt update")
        print("   sudo apt install postgresql postgresql-contrib")
        
        print("\nPara configurar a senha:")
        print("   sudo -u postgres psql")
        print("   ALTER USER postgres WITH PASSWORD '123456';")
        print("   \\q")
        
        print("\nPara iniciar o serviço:")
        print("   sudo systemctl start postgresql")
        print("   sudo systemctl enable postgresql")  # Para iniciar no boot

def main():
    """Função principal."""
    print_header("DIAGNÓSTICO POSTGRESQL - FIX CONNECTION REFUSED")
    print("Este script diagnostica e tenta resolver problemas com o PostgreSQL.")
    
    # Verificando requisitos
    try:
        import psycopg2
    except ImportError:
        print_error("O módulo psycopg2 não está instalado")
        print_info("Instalando psycopg2-binary...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
            print_success("psycopg2-binary instalado com sucesso")
            try:
                import psycopg2
            except ImportError:
                print_error("Falha ao importar psycopg2 após instalação")
                print_info("Por favor, instale manualmente: pip install psycopg2-binary")
                return
        except Exception as e:
            print_error(f"Erro ao instalar psycopg2-binary: {e}")
            print_info("Por favor, instale manualmente: pip install psycopg2-binary")
            return
    
    # Criar diretório utils
    create_utils_dir()
    
    # Verificar status do PostgreSQL
    print_info("Verificando status do PostgreSQL...")
    pg_status = get_postgresql_status()
    
    if pg_status["installed"]:
        print_success("PostgreSQL está instalado")
        if pg_status["version"]:
            print_info(f"Versão: {pg_status['version']}")
    else:
        print_error("PostgreSQL não parece estar instalado")
        show_installation_instructions()
        return
    
    if pg_status["running"]:
        print_success("Serviço PostgreSQL está em execução")
    else:
        print_error("Serviço PostgreSQL não está em execução")
    
    if pg_status["port_open"]:
        print_success("Porta 5432 está aberta e aceitando conexões")
    else:
        print_error("Porta 5432 não está acessível")
    
    # Tenta conectar ao banco
    connection_ok = test_database_connection()
    
    if connection_ok:
        print_success("Conexão ao banco de dados bem-sucedida!")
        print_header("TUDO PRONTO!")
        print("O PostgreSQL está instalado, rodando e aceitando conexões.")
        print("Agora você pode executar sua aplicação com:")
        print("   python main.py")
        return
    else:
        print_error("Não foi possível conectar ao banco de dados")
        
        # Tenta corrigir problemas
        fixed = fix_postgresql_problems()
        
        if fixed:
            print_header("PROBLEMA RESOLVIDO!")
            print("O PostgreSQL agora está funcionando corretamente.")
            print("Você pode executar sua aplicação com:")
            print("   python main.py")
        else:
            # Mostrar soluções manuais
            show_manual_solutions()

if __name__ == "__main__":
    main()