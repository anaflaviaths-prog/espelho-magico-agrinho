# 🌾 Espelho Mágico Agrinho

Aplicativo desktop interativo para a **Feira Agrinho 2026** da Escola Municipal Prefeito Durval Wolff do Amaral.

Uma experiência imersiva onde visitantes se veem em tempo real ao lado dos personagens oficiais do Agrinho, com animações, efeitos visuais e captura automática de fotos.

## 📋 Características

✨ **Interface moderna e colorida** - Inspirada na natureza (verde, amarelo, azul)
📷 **Detecção de rosto em tempo real** - Usando MediaPipe
🎭 **Personagens animados** - Suporte a múltiplos personagens PNG
🎨 **Cenários dinâmicos** - Fazenda, Escola, Horta, Natureza, Agro sustentável, Ervateria
✨ **Efeitos visuais** - Folhas caindo, sementes voando, flores, borboletas
📸 **Captura automática** - Com moldura personalizada
🔊 **Efeitos sonoros** - Opcionais e controláveis
💾 **Galeria de fotos** - Visualização das fotos capturadas
⚙️ **Configurações** - Câmera, resolução, efeitos, sons

## 🛠️ Tecnologias

- **Python 3.12+**
- **OpenCV** - Processamento de vídeo
- **MediaPipe** - Detecção de rosto e corpo
- **Pillow** - Processamento de imagens
- **CustomTkinter** - Interface moderna
- **Pygame** - Efeitos sonoros
- **PyInstaller** - Geração de executável

## 📁 Estrutura do Projeto

```
espelho-magico-agrinho/
├── main.py
├── interface.py
├── camera.py
├── detector.py
├── personagens.py
├── cenarios.py
├── efeitos.py
├── captura.py
├── moldura.py
├── configuracoes.py
├── utilitarios.py
├── requirements.txt
├── build_exe.py
├── personagens/
├── cenarios/
├── molduras/
├── efeitos/
├── sons/
├── fontes/
├── fotos/
└── assets/
```

## 🚀 Instalação

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative: `venv\Scripts\activate`
4. Instale dependências: `pip install -r requirements.txt`
5. Execute: `python main.py`

## 📦 Gerar Executável

```bash
python build_exe.py
```

---

**Tema:** "Entre Sementes e Sabores: o Caminho do Agro até a Merenda Escolar" ��🍎