# Documentação Técnica - Espelho Mágico Agrinho

## Arquitetura do Projeto

### Estrutura de Módulos

```
espelho-magico-agrinho/
├── main.py                 # Ponto de entrada do aplicativo
├── interface.py            # Interface gráfica (CustomTkinter)
├── camera.py              # Gerenciamento de câmera (OpenCV)
├── detector.py            # Detecção de rosto (MediaPipe)
├── personagens.py         # Gerenciamento de personagens
├── cenarios.py            # Gerenciamento de cenários
├── efeitos.py             # Sistema de efeitos visuais
├── captura.py             # Captura de fotos
├── moldura.py             # Criação de molduras
├── som.py                 # Gerenciamento de áudio (Pygame)
├── configuracoes.py       # Sistema de configurações (JSON)
├── utilitarios.py         # Funções auxiliares
├── build_exe.py           # Script para gerar executável
├── requirements.txt       # Dependências Python
├── config.json            # Arquivo de configuração (auto-gerado)
├── README.md              # Documentação principal
├── INSTALL.md             # Guia de instalação
├── USAGE.md               # Guia de uso
└── [PASTAS]
    ├── personagens/       # Imagens dos personagens PNG
    ├── cenarios/         # Imagens de cenários JPG/PNG
    ├── efeitos/          # Recursos de efeitos
    ├── sons/             # Arquivos de áudio WAV/MP3/OGG
    ├── molduras/         # Molduras personalizadas
    ├── fontes/           # Fontes TTF
    ├── fotos/            # Fotos capturadas (auto-criado)
    └── assets/           # Logo e ícone
```

## Fluxo de Funcionamento

### 1. Inicialização
```
main.py
  ↓
Interface()
  ↓
Camera.conectar()
Detector(MediaPipe)
GerenciadorPersonagens.carregar_personagens()
GerenciadorCenarios.carregar_cenarios()
GerenciadorEfeitos.inicializar()
GerenciadorSom.carregar_sons()
  ↓
Interface.executar() [Tkinter mainloop]
```

### 2. Loop de Captura de Vídeo
```
Camera.capturar_frame()
  ↓
Detector.detectar_rostos()
  ↓
GerenciadorPersonagens.desenhar_personagens()
  ↓
GerenciadorEfeitos.desenhar() + atualizar()
  ↓
GerenciadorCenarios.obter_cenario_redimensionado()
  ↓
Converter BGR → RGB
Redimensionar para exibição
Converter para PhotoImage (Tkinter)
  ↓
frame_video.configure(image=img_tk)
```

### 3. Captura de Foto
```
Usuário clica "Capturar Foto"
  ↓
Captura.capturar_frame(frame)
  ↓
Contagem regressiva: 3 → 2 → 1 → 0
  ↓
Captura.salvar_foto()
  ↓
Moldura.criar_moldura_agrinho()
  ↓
Salvar em fotos/AAAA-MM-DD_HH-MM-SS.png
  ↓
Reproducir som de sucesso
Mostrar mensagem de confirmação
```

## Tecnologias Utilizadas

### Core
- **Python 3.12+** - Linguagem principal
- **OpenCV (cv2)** - Processamento de vídeo
- **MediaPipe** - Detecção de rostos e landmarks
- **Pillow (PIL)** - Processamento de imagens

### Interface
- **CustomTkinter** - UI moderna e temática
- **Tkinter** - Framework GUI base

### Áudio
- **Pygame** - Reprodução de som

### Utilitários
- **NumPy** - Operações de arrays
- **JSON** - Armazenamento de configuração
- **OS/Path** - Manipulação de arquivos

### Deploy
- **PyInstaller** - Geração de executável

## Detalhes Técnicos Importantes

### Detecção de Rosto (MediaPipe)

```python
Detector.detectar_rostos(frame)
# Retorna:
# [
#   {
#     'x': int,        # Posição X
#     'y': int,        # Posição Y
#     'largura': int,  # Largura do bbox
#     'altura': int,   # Altura do bbox
#     'confianca': float,  # 0-1
#     'centro': (x, y)    # Centro do rosto
#   }
# ]
```

### Sistema de Efeitos

**Tipos de Efeitos:**
- Folhas caindo (verde)
- Sementes voando (marrom)
- Flores (variadas)
- Brilho (branco)

**Cada efeito usa:**
- Classe `Particula` com física básica
- Gravidade (vy += 0.1)
- Opacidade baseada em vida restante
- Remocao automática quando vida <= 0

### Processamento de Imagem

**Redimensionamento com proporção:**
```python
Utilitarios.redimensionar_imagem(
    imagem,
    largura=800,
    altura=None,
    manter_proporcao=True
)
```

**Blending de personagens (RGBA):**
```python
mascara = imagem[:, :, 3] / 255.0
cores = imagem[:, :, :3]
regiao = fundo
regiao = cores * mascara + regiao * (1 - mascara)
```

### Configuração (JSON)

**Estrutura padrão:**
```json
{
  "camera": 0,
  "resolucao": "1280x720",
  "tempo_contagem": 3,
  "efeitos_visuais": true,
  "musica": true,
  "sons": true,
  "brilho": 1.0,
  "contraste": 1.0,
  "cenario_padrao": "fazenda",
  "personagens": true,
  "animacoes": true,
  "volume": 70,
  "fullscreen": true,
  "pixelacao": false,
  "modo_escuro": true
}
```

## Performance

### Otimizações Implementadas

1. **Captura de Vídeo em Thread Separada**
   - Loop principal não bloqueia UI
   - ~30 FPS mantido

2. **Redimensionamento Inteligente**
   - Frame redimensionado apenas para exibição
   - Original mantém resolução completa

3. **Lazy Loading de Imagens**
   - Personagens carregados sob demanda
   - Cenários carregados na inicialização

4. **Remoção de Partículas Inativas**
   - Limpeza automática de efeitos inativos
   - Evita acúmulo de memória

5. **Switches de Efeitos**
   - Desativar efeitos reduz CPU em ~30%
   - Desativar sons libera recursos Pygame

### Uso de Memória

- **Frame em memória:** ~6-10 MB (1280x720)
- **Personagens carregados:** ~2-5 MB cada
- **Cenários carregados:** ~8-15 MB cada
- **Memória total em uso:** ~50-150 MB

## Segurança e Privacidade

### Fotos Capturadas
- Salvas localmente em `fotos/`
- Nenhum envio para servidor
- Nenhuma coleta de dados pessoais
- Usuário tem controle total

### Configurações
- Armazenadas em `config.json` local
- Sem sincronização em nuvem
- Sem envio de telemetria

## Customização

### Adicionar Novo Personagem

1. **Preparar PNG com fundo transparente**
2. **Copiar para `personagens/nome.png`**
3. **Aplicativo carrega automaticamente**

```python
# No gerenciador:
gm.listar_personagens()  # Retorna lista de nomes
gm.adicionar_personagem_ativo("nome", x=100, y=100, escala=0.3)
```

### Adicionar Novo Cenário

1. **Preparar JPG/PNG em alta resolução**
2. **Copiar para `cenarios/nome.jpg`**
3. **Definir como ativo:**

```python
gm_cenarios.definir_cenario_ativo("nome")
frame_cenario = gm_cenarios.obter_cenario_redimensionado(1280, 720)
```

### Adicionar Som

1. **Copiar WAV/MP3/OGG para `sons/nome.wav`**
2. **Reproduzir:**

```python
gm_som.reproduzir_som("nome")
```

## Resolução de Problemas Técnicos

### FPS Baixo
- Desabilitar efeitos: `config.json` → `efeitos_visuais: false`
- Reduzir resolução: `config.json` → `resolucao: 640x480`
- Fechar aplicativos em background

### Câmera não funciona
- Verificar ID da câmera: `Camera.listar_cameras_disponiveis()`
- Ajustar em `config.json` → `camera: 0` (mudar para 1, 2, etc)

### Sons não tocam
- Verificar arquivos em `sons/`
- Testar volume do sistema
- Verificar permissões de arquivo

## Build para Executável

```bash
# Gera .exe standalone
python build_exe.py

# Resultado em:
dist/EspelhoMagicoAgrinho.exe

# Tamanho: ~150-200 MB
```

## Roadmap de Melhorias

- [ ] Suporte a múltiplos rostos
- [ ] Animações de personagens
- [ ] Seleção dinâmica de cenários
- [ ] Editor de molduras
- [ ] Câmera para rede (streaming)
- [ ] Galeria integrada
- [ ] Filtros de câmera
- [ ] Integração com redes sociais
- [ ] Suporte a múltiplos idiomas
- [ ] Modo dark/light theme toggle

## Licença e Créditos

**Desenvolvido para:** Feira Agrinho 2026
**Escola:** Escola Municipal Prefeito Durval Wolff do Amaral
**Tema:** "Entre Sementes e Sabores: o Caminho do Agro até a Merenda Escolar"

### Dependências
- OpenCV (BSD License)
- MediaPipe (Apache 2.0)
- CustomTkinter (MIT License)
- Pygame (LGPL)
- Pillow (HPND)
- NumPy (BSD License)

---

**Versão:** 1.0.0  
**Data:** 24 de Julho de 2026  
**Desenvolvedor:** @anaflaviaths-prog
