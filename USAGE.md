# Guia de Uso - Espéculo Mágico Agrinho

## Primeiros Passos

### 1. Iniciar o Aplicativo

Execute um dos seguintes comandos:

**Versão Python:**
```bash
python main.py
```

**Versão Executável:**
Duplo clique em `EspelhoMagicoAgrinho.exe`

### 2. Tela Principal

Você verá a interface com:
- Título "Espéculo Mágico Agrinho"
- Preview da câmera (vazio inicialmente)
- Botões de controle
- Opções de configuração

## Como Usar

### Capturar uma Foto

1. **Clique em "Iniciar"**
   - A câmera será ativada
   - Você verá sua imagem em tempo real
   - Os personagens aparecerão na tela

2. **Posicione-se**
   - Fique frente à câmera
   - Deixe o rosto visível
   - Centralize seu rosto na moldura

3. **Clique em "Capturar Foto"**
   - Uma contagem regressiva começará (padrão: 3 segundos)
   - Prepare-se para a captura
   - A foto será capturada automaticamente

4. **Resultado**
   - A foto será processada com moldura
   - Salva em `fotos/AAAA-MM-DD_HH-MM-SS.png`
   - Uma mensagem de confirmação aparecerá

### Parar o Aplicativo

Clique em "Parar" para desconectar a câmera ou "Sair" para fechar o aplicativo.

## Configurações

### Efeitos Visuais

- **Ativar/Desativar:** Use o switch "Efeitos Visuais"
- Inclui: folhas caindo, sementes voando, flores, brilho
- Desativar reduz uso de CPU

### Sons

- **Ativar/Desativar:** Use o switch "Sons"
- Sons incluem: clique, captura, sucesso
- Necessário ter arquivos de som em `sons/`

### Outras Opções (Config JSON)

Edite `config.json` para customizar:

```json
{
  "camera": 0,              // ID da câmera
  "resolucao": "1280x720",  // Resolução
  "tempo_contagem": 3,      // Segundos para captura
  "efeitos_visuais": true,  // Efeitos on/off
  "sons": true,             // Sons on/off
  "fullscreen": true,       // Tela cheia
  "volume": 70              // Volume (0-100)
}
```

## Onde estão as Fotos?

Todas as fotos capturadas são salvas em:
```
fotos/
  2026-07-24_14-30-45.png
  2026-07-24_14-31-20.png
  ...
```

## Adicionando Novos Personagens

1. Prepare uma imagem PNG com fundo transparente
2. Copie para a pasta `personagens/`
3. O aplicativo carrega automaticamente na próxima execução

Exemplo:
```
personagens/
  menina.png
  menino.png
  seu_personagem.png  <- Será carregado automaticamente
```

## Adicionando Novos Cenários

1. Prepare uma imagem JPG ou PNG em alta resolução
2. Copie para a pasta `cenarios/`
3. O aplicativo carrega automaticamente na próxima execução

Exemplo:
```
centarios/
  fazenda.jpg
  escola.jpg
  seu_cenario.jpg  <- Será carregado automaticamente
```

## Dicas e Truques

### Melhor Qualidade de Foto

- Aumente a resolução em `config.json`
- Use boa iluminação
- Aumente o tempo de contagem para mais tempo de preparo

### Melhor Performance

- Desative efeitos visuais se o PC for lento
- Reduza a resolução
- Feche outros programas

### Personalização

- Adicione música de fundo em `sons/background.mp3`
- Crie molduras personalizadas em `molduras/`
- Customize cores e temas no código

## Suporte

Para dúvidas ou problemas:
1. Verifique `INSTALL.md` para instalação
2. Abra uma issue no GitHub
3. Verifique a seção "Resolução de Problemas"

---

**Desenvolvido para a Feira Agrinho 2026 da Escola Municipal Prefeito Durval Wolff do Amaral**

🌾 Entre Sementes e Sabores: o Caminho do Agro até a Merenda Escolar 🍎
