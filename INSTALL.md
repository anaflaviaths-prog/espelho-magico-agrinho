# Instruções de Instalação - Espéculo Mágico Agrinho

## Pré-requisitos

- Windows 10 ou Windows 11
- Python 3.12 ou superior
- Webcam
- ~500 MB de espaço em disco

## Instalação Passo a Passo

### 1. Instalar Python

Baixe Python 3.12+ em: https://www.python.org/downloads/

**IMPORTANTE:** Marque a opção "Add Python to PATH" durante a instalação

### 2. Clonar o Repositório

```bash
git clone https://github.com/anaflaviaths-prog/espelho-magico-agrinho.git
cd espelho-magico-agrinho
```

Ou baixe o ZIP diretamente do repositório.

### 3. Criar Ambiente Virtual

```bash
python -m venv venv
```

### 4. Ativar Ambiente Virtual

**No PowerShell:**
```bash
.\venv\Scripts\Activate.ps1
```

**No Prompt de Comando (CMD):**
```bash
venv\Scripts\activate.bat
```

### 5. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 6. Preparar Assets

Copie os arquivos para as respectivas pastas:

- **Personagens:** Coloque imagens PNG dos personagens em `personagens/`
- **Cenários:** Coloque imagens JPG/PNG em `cenarios/`
- **Sons:** Coloque arquivos WAV/MP3 em `sons/`
- **Logo/Ícone:** Coloque em `assets/`

### 7. Executar o Aplicativo

```bash
python main.py
```

## Gerar Executável (Opcional)

Para criar um arquivo `.exe` standalone:

```bash
python build_exe.py
```

O executável será gerado em `dist/EspelhoMagicoAgrinho.exe`

## Resolução de Problemas

### Erro: "Câmera não encontrada"

- Verifique se a webcam está conectada
- Teste a webcam com outro programa
- Verifique permissões de acesso

### Erro: "Modulo não encontrado"

Certifique-se de que o ambiente virtual está ativado:
```bash
venv\Scripts\activate.bat
```

E reinstale as dependências:
```bash
pip install -r requirements.txt
```

### Interface não responde

- Tente desativar efeitos visuais
- Reduza a resolução em Configurações
- Verifique desempenho do computador

## Suporte

Para problemas ou dúvidas, abra uma issue no repositório GitHub.

---

**Desenvolvido para a Feira Agrinho 2026**
