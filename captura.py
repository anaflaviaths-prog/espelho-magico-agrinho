"""
Módulo de Captura
Responsável pela captura de fotos e screenshots
"""

import cv2
import numpy as np
from utilitarios import Utilitarios
from typing import Optional
import os


class Captura:
    """
    Classe para capturar e salvar fotos.
    """
    
    def __init__(self):
        """
        Inicializa o sistema de captura.
        """
        Utilitarios.criar_diretorios()
        self.ultima_foto = None
        self.caminho_ultima_foto = None
    
    def capturar_frame(self, frame: np.ndarray) -> bool:
        """
        Captura um frame e o armazena na memória.
        
        Args:
            frame: Frame a ser capturado
            
        Returns:
            True se capturado com sucesso, False caso contrário
        """
        try:
            self.ultima_foto = frame.copy()
            return True
        except Exception as e:
            print(f"Erro ao capturar frame: {e}")
            return False
    
    def salvar_foto(self, frame: np.ndarray = None, qualidade: int = 95) -> Optional[str]:
        """
        Salva a foto no disco.
        
        Args:
            frame: Frame a ser salvo (se None, usa última captura)
            qualidade: Qualidade da imagem PNG (0-100)
            
        Returns:
            Caminho da foto salva ou None se erro
        """
        try:
            if frame is None:
                frame = self.ultima_foto
            
            if frame is None:
                print("Nenhuma foto para salvar")
                return None
            
            caminho_completo = Utilitarios.caminho_foto_completo()
            
            # Garante que o diretório existe
            os.makedirs(Utilitarios.PASTA_FOTOS, exist_ok=True)
            
            # Salva a imagem
            sucesso = cv2.imwrite(caminho_completo, frame, [cv2.IMWRITE_PNG_COMPRESSION, 9])
            
            if sucesso:
                self.caminho_ultima_foto = caminho_completo
                print(f"Foto salva em: {caminho_completo}")
                return caminho_completo
            else:
                print(f"Erro ao salvar foto em: {caminho_completo}")
                return None
        
        except Exception as e:
            print(f"Erro ao salvar foto: {e}")
            return None
    
    def obter_ultima_foto(self) -> Optional[np.ndarray]:
        """
        Obtém a última foto capturada na memória.
        
        Returns:
            Frame da última foto ou None
        """
        return self.ultima_foto.copy() if self.ultima_foto is not None else None
    
    def obter_caminho_ultima_foto(self) -> Optional[str]:
        """
        Obtém o caminho da última foto salva.
        
        Returns:
            Caminho da foto ou None
        """
        return self.caminho_ultima_foto
    
    def limpar(self) -> None:
        """
        Limpa a foto em cache da memória.
        """
        self.ultima_foto = None
