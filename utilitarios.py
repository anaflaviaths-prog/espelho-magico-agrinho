"""
Módulo de Utilitários
Funções auxiliares para o aplicativo Espelho Mágico Agrinho
"""

import os
from pathlib import Path
from typing import Tuple
from datetime import datetime
import cv2
import numpy as np


class Utilitarios:
    """Classe com funções utilitárias do aplicativo."""
    
    # Diretórios principais
    PASTA_PERSONAGENS = "personagens"
    PASTA_CENARIOS = "cenarios"
    PASTA_EFEITOS = "efeitos"
    PASTA_SONS = "sons"
    PASTA_MOLDURAS = "molduras"
    PASTA_FONTES = "fontes"
    PASTA_FOTOS = "fotos"
    PASTA_ASSETS = "assets"
    
    @staticmethod
    def criar_diretorios() -> None:
        """Cria os diretórios necessários se não existirem."""
        diretorios = [
            Utilitarios.PASTA_PERSONAGENS,
            Utilitarios.PASTA_CENARIOS,
            Utilitarios.PASTA_EFEITOS,
            Utilitarios.PASTA_SONS,
            Utilitarios.PASTA_MOLDURAS,
            Utilitarios.PASTA_FONTES,
            Utilitarios.PASTA_FOTOS,
            Utilitarios.PASTA_ASSETS,
        ]
        
        for diretorio in diretorios:
            Path(diretorio).mkdir(exist_ok=True)
    
    @staticmethod
    def gerar_nome_arquivo_foto() -> str:
        """
        Gera o nome do arquivo de foto baseado em data e hora.
        Formato: AAAA-MM-DD_HH-MM-SS.png
        
        Returns:
            Nome do arquivo
        """
        agora = datetime.now()
        nome = agora.strftime("%Y-%m-%d_%H-%M-%S")
        return f"{nome}.png"
    
    @staticmethod
    def caminho_foto_completo() -> str:
        """
        Retorna o caminho completo do arquivo de foto a ser salvo.
        
        Returns:
            Caminho completo
        """
        Utilitarios.criar_diretorios()
        nome_arquivo = Utilitarios.gerar_nome_arquivo_foto()
        return os.path.join(Utilitarios.PASTA_FOTOS, nome_arquivo)
    
    @staticmethod
    def listar_personagens() -> list:
        """
        Lista todos os personagens disponíveis.
        
        Returns:
            Lista de caminhos dos personagens PNG
        """
        Utilitarios.criar_diretorios()
        personagens = []
        
        if os.path.exists(Utilitarios.PASTA_PERSONAGENS):
            for arquivo in os.listdir(Utilitarios.PASTA_PERSONAGENS):
                if arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
                    caminho = os.path.join(Utilitarios.PASTA_PERSONAGENS, arquivo)
                    personagens.append(caminho)
        
        return sorted(personagens)
    
    @staticmethod
    def listar_cenarios() -> list:
        """
        Lista todos os cenários disponíveis.
        
        Returns:
            Lista de caminhos dos cenários
        """
        Utilitarios.criar_diretorios()
        cenarios = []
        
        if os.path.exists(Utilitarios.PASTA_CENARIOS):
            for arquivo in os.listdir(Utilitarios.PASTA_CENARIOS):
                if arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                    caminho = os.path.join(Utilitarios.PASTA_CENARIOS, arquivo)
                    cenarios.append(caminho)
        
        return sorted(cenarios)
    
    @staticmethod
    def listar_sons() -> dict:
        """
        Lista todos os sons disponíveis.
        
        Returns:
            Dicionário com nome e caminho dos sons
        """
        Utilitarios.criar_diretorios()
        sons = {}
        
        if os.path.exists(Utilitarios.PASTA_SONS):
            for arquivo in os.listdir(Utilitarios.PASTA_SONS):
                if arquivo.lower().endswith(('.wav', '.mp3', '.ogg')):
                    nome = os.path.splitext(arquivo)[0]
                    caminho = os.path.join(Utilitarios.PASTA_SONS, arquivo)
                    sons[nome] = caminho
        
        return sons
    
    @staticmethod
    def redimensionar_imagem(
        imagem: np.ndarray,
        largura: int = None,
        altura: int = None,
        manter_proporcao: bool = True
    ) -> np.ndarray:
        """
        Redimensiona uma imagem.
        
        Args:
            imagem: Imagem OpenCV (numpy array)
            largura: Largura desejada
            altura: Altura desejada
            manter_proporcao: Se True, mantém a proporção da imagem
            
        Returns:
            Imagem redimensionada
        """
        if imagem is None:
            return None
        
        altura_original, largura_original = imagem.shape[:2]
        
        if largura is None and altura is None:
            return imagem
        
        if manter_proporcao:
            if largura is not None and altura is None:
                escala = largura / largura_original
                altura = int(altura_original * escala)
            elif altura is not None and largura is None:
                escala = altura / altura_original
                largura = int(largura_original * escala)
        
        return cv2.resize(imagem, (largura, altura), interpolation=cv2.INTER_AREA)
    
    @staticmethod
    def converter_resolucao_string(resolucao_str: str) -> Tuple[int, int]:
        """
        Converte string de resolução para tupla (largura, altura).
        
        Args:
            resolucao_str: String no formato "WIDTHxHEIGHT" (ex: "1280x720")
            
        Returns:
            Tupla (largura, altura)
        """
        try:
            largura, altura = map(int, resolucao_str.lower().split('x'))
            return (largura, altura)
        except (ValueError, AttributeError):
            return (1280, 720)  # Valor padrão
    
    @staticmethod
    def desenhar_retangulo_arredondado(
        imagem: np.ndarray,
        pt1: Tuple[int, int],
        pt2: Tuple[int, int],
        cor: Tuple[int, int, int],
        espessura: int = 2,
        raio: int = 20
    ) -> np.ndarray:
        """
        Desenha um retângulo com cantos arredondados.
        
        Args:
            imagem: Imagem OpenCV
            pt1: Ponto superior esquerdo (x, y)
            pt2: Ponto inferior direito (x, y)
            cor: Cor em BGR
            espessura: Espessura da linha
            raio: Raio dos cantos
            
        Returns:
            Imagem com retângulo desenhado
        """
        x1, y1 = pt1
        x2, y2 = pt2
        
        # Desenha as linhas
        cv2.line(imagem, (x1 + raio, y1), (x2 - raio, y1), cor, espessura)
        cv2.line(imagem, (x1 + raio, y2), (x2 - raio, y2), cor, espessura)
        cv2.line(imagem, (x1, y1 + raio), (x1, y2 - raio), cor, espessura)
        cv2.line(imagem, (x2, y1 + raio), (x2, y2 - raio), cor, espessura)
        
        # Desenha os cantos arredondados
        cv2.ellipse(imagem, (x1 + raio, y1 + raio), (raio, raio), 180, 0, 90, cor, espessura)
        cv2.ellipse(imagem, (x2 - raio, y1 + raio), (raio, raio), 90, 0, 90, cor, espessura)
        cv2.ellipse(imagem, (x1 + raio, y2 - raio), (raio, raio), 270, 0, 90, cor, espessura)
        cv2.ellipse(imagem, (x2 - raio, y2 - raio), (raio, raio), 0, 0, 90, cor, espessura)
        
        return imagem
    
    @staticmethod
    def aplicar_blur_fundo(imagem: np.ndarray, mascara: np.ndarray, intensidade: int = 21) -> np.ndarray:
        """
        Aplica blur no fundo de uma imagem usando máscara.
        
        Args:
            imagem: Imagem OpenCV
            mascara: Máscara binária
            intensidade: Intensidade do blur (deve ser ímpar)
            
        Returns:
            Imagem com fundo desfocado
        """
        if intensidade % 2 == 0:
            intensidade += 1
        
        fundo_blur = cv2.GaussianBlur(imagem, (intensidade, intensidade), 0)
        mascara_invertida = cv2.bitwise_not(mascara)
        
        fundo = cv2.bitwise_and(fundo_blur, fundo_blur, mask=mascara_invertida)
        frente = cv2.bitwise_and(imagem, imagem, mask=mascara)
        
        return cv2.add(fundo, frente)
    
    @staticmethod
    def brilho_contraste(imagem: np.ndarray, brilho: float = 1.0, contraste: float = 1.0) -> np.ndarray:
        """
        Ajusta brilho e contraste de uma imagem.
        
        Args:
            imagem: Imagem OpenCV
            brilho: Fator de brilho (1.0 = normal)
            contraste: Fator de contraste (1.0 = normal)
            
        Returns:
            Imagem com ajustes aplicados
        """
        imagem = cv2.convertScaleAbs(imagem, alpha=contraste, beta=0)
        imagem = cv2.convertScaleAbs(imagem, alpha=1.0, beta=(brilho - 1.0) * 255)
        return imagem
    
    @staticmethod
    def validar_caminho_arquivo(caminho: str) -> bool:
        """
        Valida se o caminho é um arquivo que existe.
        
        Args:
            caminho: Caminho do arquivo
            
        Returns:
            True se o arquivo existe, False caso contrário
        """
        return os.path.isfile(caminho) and os.path.exists(caminho)
    
    @staticmethod
    def validar_caminho_diretorio(caminho: str) -> bool:
        """
        Valida se o caminho é um diretório que existe.
        
        Args:
            caminho: Caminho do diretório
            
        Returns:
            True se o diretório existe, False caso contrário
        """
        return os.path.isdir(caminho) and os.path.exists(caminho)
