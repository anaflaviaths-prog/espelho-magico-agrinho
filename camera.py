"""
Módulo de Câmera
Gerencia a captura de vídeo e acesso à webcam
"""

import cv2
from typing import Optional, Tuple
from configuracoes import config
import numpy as np


class Camera:
    """
    Classe para gerenciar a câmera e captura de vídeo.
    """
    
    def __init__(self, camera_id: int = None):
        """
        Inicializa a câmera.
        
        Args:
            camera_id: ID da câmera (0 = padrão)
        """
        self.camera_id = camera_id if camera_id is not None else config.obter("camera", 0)
        self.captura = None
        self.conectado = False
        self.largura = 1280
        self.altura = 720
    
    def conectar(self) -> bool:
        """
        Conecta à câmera.
        
        Returns:
            True se conectado com sucesso, False caso contrário
        """
        try:
            self.captura = cv2.VideoCapture(self.camera_id)
            
            if not self.captura.isOpened():
                print(f"Erro: Não foi possível abrir a câmera {self.camera_id}")
                return False
            
            # Define resolução
            resolucao_str = config.obter("resolucao", "1280x720")
            self.largura, self.altura = self._parse_resolucao(resolucao_str)
            
            self.captura.set(cv2.CAP_PROP_FRAME_WIDTH, self.largura)
            self.captura.set(cv2.CAP_PROP_FRAME_HEIGHT, self.altura)
            self.captura.set(cv2.CAP_PROP_FPS, 30)
            
            self.conectado = True
            print(f"Câmera {self.camera_id} conectada com sucesso")
            return True
        
        except Exception as e:
            print(f"Erro ao conectar câmera: {e}")
            self.conectado = False
            return False
    
    def capturar_frame(self) -> Optional[np.ndarray]:
        """
        Captura um frame da câmera.
        
        Returns:
            Frame capturado ou None se erro
        """
        if not self.conectado or self.captura is None:
            return None
        
        try:
            sucesso, frame = self.captura.read()
            if sucesso:
                return frame
            else:
                print("Erro ao capturar frame")
                return None
        except Exception as e:
            print(f"Erro ao capturar frame: {e}")
            return None
    
    def desconectar(self) -> None:
        """Desconecta a câmera."""
        if self.captura is not None:
            self.captura.release()
            self.conectado = False
            print("Câmera desconectada")
    
    def obter_dimensoes(self) -> Tuple[int, int]:
        """
        Obtém as dimensões dos frames.
        
        Returns:
            Tupla (largura, altura)
        """
        return (self.largura, self.altura)
    
    def listar_cameras_disponiveis(self) -> list:
        """
        Lista câmeras disponíveis no sistema.
        
        Returns:
            Lista com IDs das câmeras disponíveis
        """
        cameras_disponiveis = []
        
        for i in range(10):  # Verifica até 10 câmeras
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras_disponiveis.append(i)
                cap.release()
        
        return cameras_disponiveis
    
    @staticmethod
    def _parse_resolucao(resolucao_str: str) -> Tuple[int, int]:
        """
        Parse de string de resolução.
        
        Args:
            resolucao_str: String no formato "WIDTHxHEIGHT"
            
        Returns:
            Tupla (largura, altura)
        """
        try:
            largura, altura = map(int, resolucao_str.lower().split('x'))
            return (largura, altura)
        except:
            return (1280, 720)
    
    def espelhar_horizontalmente(self, frame: np.ndarray) -> np.ndarray:
        """
        Espelha o frame horizontalmente (efeito de espelho).
        
        Args:
            frame: Frame original
            
        Returns:
            Frame espelhado
        """
        return cv2.flip(frame, 1)
    
    def __del__(self):
        """Garante que a câmera seja desconectada ao destruir o objeto."""
        self.desconectar()
