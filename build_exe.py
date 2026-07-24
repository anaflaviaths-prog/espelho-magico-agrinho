"""
Script para gerar executável (.exe) usando PyInstaller
"""

import subprocess
import sys
import os


def criar_executavel():
    """
    Cria um executável Windows usando PyInstaller.
    """
    
    print("="*60)
    print("💥 Gerando Executável do Espelho Mágico Agrinho")
    print("="*60)
    
    # Parâmetros do PyInstaller
    parametros = [
        "pyinstaller",
        "--onefile",  # Gera um único arquivo executável
        "--windowed",  # Sem console
        "--name=EspelhoMagicoAgrinho",  # Nome do executável
        "--icon=assets/icone.ico" if os.path.exists("assets/icone.ico") else None,  # Ícone (se existir)
        "--add-data=personagens:personagens",  # Inclui pasta de personagens
        "--add-data=cenarios:cenarios",  # Inclui pasta de cenários
        "--add-data=sons:sons",  # Inclui pasta de sons
        "--add-data=molduras:molduras",  # Inclui pasta de molduras
        "--add-data=assets:assets",  # Inclui pasta de assets
        "--hidden-import=customtkinter",
        "--hidden-import=cv2",
        "--hidden-import=mediapipe",
        "--hidden-import=PIL",
        "--hidden-import=pygame",
        "main.py"
    ]
    
    # Remove None dos parâmetros
    parametros = [p for p in parametros if p is not None]
    
    try:
        print(f"\n⚡ Executando PyInstaller...")
        resultado = subprocess.run(parametros, check=True)
        
        if resultado.returncode == 0:
            print("\n🎆 Executável criado com sucesso!")
            print("\n📁 Local: dist/EspelhoMagicoAgrinho.exe")
            print("\n🚀 Você pode distribuír este arquivo para usar em outras máquinas.")
        else:
            print(f"\n❌ Erro ao criar executável. Código: {resultado.returncode}")
    
    except FileNotFoundError:
        print("\n❌ PyInstaller não encontrado.")
        print("Instale com: pip install pyinstaller")
        sys.exit(1)
    
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao executar PyInstaller: {e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    criar_executavel()
