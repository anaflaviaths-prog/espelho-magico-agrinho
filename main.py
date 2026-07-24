"""
Módulo Principal - Ponto de Entrada
Espelho Mágico Agrinho - Aplicativo Desktop
"""

import sys
import os

# Adiciona o diretório atual ao path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interface import Interface
from utilitarios import Utilitarios
from configuracoes import config


def main():
    """
    Função principal que inicia o aplicativo.
    """
    try:
        # Cria os diretórios necessários
        Utilitarios.criar_diretorios()
        
        print("="*50)
        print("🌾 Espelho Mágico Agrinho")
        print("Feira Agrinho 2026")
        print("="*50)
        
        # Inicia a interface
        app = Interface()
        app.executar()
        
    except KeyboardInterrupt:
        print("\n\nAplicativo interrompido pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErro crítico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
