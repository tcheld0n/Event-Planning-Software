"""
Sistema de Gerenciamento de Eventos
Este script une a configuração do banco de dados e a inicialização da aplicação.
"""
import sys
from utils.create_table import criar_banco, criar_tabelas
from app import create_app

def inicializar_sistema():
    """Inicializa o sistema configurando o banco de dados e iniciando a aplicação."""
    print("\n=== Sistema de Gerenciamento de Eventos ===\n")
    
    # Configuração do banco de dados
    print("Configurando banco de dados...")
    try:
        criar_banco()
        criar_tabelas()
        print("Banco de dados configurado com sucesso!")
    except Exception as e:
        print(f"Erro ao configurar banco de dados: {e}")
        sys.exit(1)
    
    # Inicialização da aplicação Flask
    print("\nIniciando servidor web...")
    app = create_app()
    print("\nServidor iniciado! Acesse http://localhost:5000 no seu navegador.")
    
    # Inicia o servidor Flask
    app.run(debug=True)

if __name__ == "__main__":
    inicializar_sistema()