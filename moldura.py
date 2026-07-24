"""
Módulo de Moldura
Gera molduras personalizadas para as fotos capturadas
"""

import cv2
import numpy as np
from typing import Tuple, Optional
from utilitarios import Utilitarios


class Moldura:
    """
    Classe para criar molduras nas fotos.
    """
    
    def __init__(self, largura: int, altura: int):
        """
        Inicializa a moldura.
        
        Args:
            largura: Largura da moldura
            altura: Altura da moldura
        """
        self.largura = largura
        self.altura = altura
        self.espessura_moldura = 60  # Espessura em pixels
    
    def criar_moldura_simples(self, frame: np.ndarray, cor_moldura: Tuple = (34, 139, 34), cor_texto: Tuple = (255, 255, 255)) -> np.ndarray:
        """
        Cria uma moldura simples ao redor da imagem.
        
        Args:
            frame: Frame original
            cor_moldura: Cor da moldura em BGR
            cor_texto: Cor do texto em BGR
            
        Returns:
            Imagem com moldura
        """
        try:
            # Cria imagem com espaço para a moldura
            altura_total = self.altura + (self.espessura_moldura * 2)
            largura_total = self.largura + (self.espessura_moldura * 2)
            
            imagem_com_moldura = np.ones((altura_total, largura_total, 3), dtype=np.uint8)
            imagem_com_moldura[:] = cor_moldura
            
            # Redimensiona e cola a imagem original no centro
            frame_redim = Utilitarios.redimensionar_imagem(frame, self.largura, self.altura)
            if frame_redim is not None:
                imagem_com_moldura[self.espessura_moldura:self.espessura_moldura + self.altura,
                                  self.espessura_moldura:self.espessura_moldura + self.largura] = frame_redim
            
            return imagem_com_moldura
        
        except Exception as e:
            print(f"Erro ao criar moldura simples: {e}")
            return frame
    
    def adicionar_texto_moldura(self, frame: np.ndarray, textos: list, cor: Tuple = (255, 255, 255)) -> np.ndarray:
        """
        Adiciona texto na moldura.
        
        Args:
            frame: Imagem com moldura
            textos: Lista de strings com o texto
            cor: Cor do texto em BGR
            
        Returns:
            Imagem com texto adicionado
        """
        try:
            frame_copia = frame.copy()
            fonte = cv2.FONT_HERSHEY_SIMPLEX
            tamanho_fonte = 1.0
            espessura_fonte = 2
            margem = 20
            
            y_posicao = self.espessura_moldura // 2 + 15
            
            for texto in textos:
                # Obtém o tamanho do texto
                (largura_texto, altura_texto), _ = cv2.getTextSize(texto, fonte, tamanho_fonte, espessura_fonte)
                
                # Centraliza horizontalmente
                x_posicao = (frame.shape[1] - largura_texto) // 2
                
                # Escreve o texto
                cv2.putText(frame_copia, texto, (x_posicao, y_posicao),
                           fonte, tamanho_fonte, cor, espessura_fonte)
                
                y_posicao += altura_texto + margem
            
            return frame_copia
        
        except Exception as e:
            print(f"Erro ao adicionar texto: {e}")
            return frame
    
    def criar_moldura_agrinho(self, frame: np.ndarray) -> np.ndarray:
        """
        Cria a moldura personalizada para a Feira Agrinho 2026.
        
        Args:
            frame: Frame original
            
        Returns:
            Imagem com moldura Agrinho
        """
        try:
            # Primeiro cria a moldura
            moldura = self.criar_moldura_simples(frame, cor_moldura=(34, 139, 34))
            
            # Depois adiciona o texto
            textos = [
                "Feira Agrinho 2026",
                "Escola Municipal Prefeit\u0364ura Durval Wolff do Amaral",
                "Entre Sementes e Sabores: o Caminho do Agro at\u00e9 a Merenda Escolar"
            ]
            
            moldura_com_texto = self.adicionar_texto_moldura(moldura, textos)
            
            return moldura_com_texto
        
        except Exception as e:
            print(f"Erro ao criar moldura Agrinho: {e}")
            return frame
    
    def adicionar_borda_colorida(self, frame: np.ndarray, cor: Tuple = (0, 255, 0), espessura: int = 5) -> np.ndarray:
        """
        Adiciona uma borda colorida ao redor da imagem.
        
        Args:
            frame: Imagem
            cor: Cor da borda em BGR
            espessura: Espessura da borda
            
        Returns:
            Imagem com borda
        """
        cv2.rectangle(frame, (0, 0), (frame.shape[1] - 1, frame.shape[0] - 1), cor, espessura)
        return frame
