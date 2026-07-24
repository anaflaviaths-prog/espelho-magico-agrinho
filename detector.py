"""
Módulo de Detector
Detecção de rosto e landmarks usando MediaPipe
"""

import mediapipe as mp
import cv2
import numpy as np
from typing import Optional, Tuple, List


class Detector:
    """
    Classe para detecção de rosto e landmarks usando MediaPipe.
    """
    
    def __init__(self):
        """
        Inicializa o detector.
        """
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,  # 1 para faces mais distantes
            min_detection_confidence=0.5
        )
        
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=5,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def detectar_rostos(self, frame: np.ndarray) -> Optional[list]:
        """
        Detecta rostos em um frame.
        
        Args:
            frame: Frame do vídeo
            
        Returns:
            Lista com informações dos rostos detectados ou None
        """
        try:
            h, w, c = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resultados = self.face_detection.process(frame_rgb)
            
            if resultados.detections:
                rostos = []
                for deteccao in resultados.detections:
                    bbox = deteccao.location_data.relative_bounding_box
                    x = int(bbox.xmin * w)
                    y = int(bbox.ymin * h)
                    largura = int(bbox.width * w)
                    altura = int(bbox.height * h)
                    confianca = deteccao.score[0]
                    
                    rostos.append({
                        'x': x,
                        'y': y,
                        'largura': largura,
                        'altura': altura,
                        'confianca': confianca,
                        'centro': (x + largura // 2, y + altura // 2)
                    })
                
                return rostos
            return None
        
        except Exception as e:
            print(f"Erro ao detectar rostos: {e}")
            return None
    
    def detectar_landmarks(self, frame: np.ndarray) -> Optional[list]:
        """
        Detecta landmarks (pontos) do rosto.
        
        Args:
            frame: Frame do vídeo
            
        Returns:
            Lista com landmarks dos rostos ou None
        """
        try:
            h, w, c = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resultados = self.face_mesh.process(frame_rgb)
            
            if resultados.multi_face_landmarks:
                landmarks_lista = []
                for face_landmarks in resultados.multi_face_landmarks:
                    landmarks = []
                    for landmark in face_landmarks.landmark:
                        x = int(landmark.x * w)
                        y = int(landmark.y * h)
                        z = landmark.z
                        landmarks.append((x, y, z))
                    landmarks_lista.append(landmarks)
                
                return landmarks_lista
            return None
        
        except Exception as e:
            print(f"Erro ao detectar landmarks: {e}")
            return None
    
    def desenhar_caixa_rosto(self, frame: np.ndarray, rostos: list, cor: Tuple = (0, 255, 0), espessura: int = 2) -> np.ndarray:
        """
        Desenha caixas ao redor dos rostos detectados.
        
        Args:
            frame: Frame do vídeo
            rostos: Lista de rostos detectados
            cor: Cor da caixa em BGR
            espessura: Espessura da linha
            
        Returns:
            Frame com caixas desenhadas
        """
        if rostos is None:
            return frame
        
        frame_copia = frame.copy()
        for rosto in rostos:
            x, y = rosto['x'], rosto['y']
            w, h = rosto['largura'], rosto['altura']
            cv2.rectangle(frame_copia, (x, y), (x + w, y + h), cor, espessura)
        
        return frame_copia
    
    def desenhar_landmarks(self, frame: np.ndarray, landmarks: list, cor: Tuple = (0, 255, 0), raio: int = 2) -> np.ndarray:
        """
        Desenha landmarks no frame.
        
        Args:
            frame: Frame do vídeo
            landmarks: Lista de landmarks
            cor: Cor dos pontos em BGR
            raio: Raio dos pontos
            
        Returns:
            Frame com landmarks desenhados
        """
        if landmarks is None:
            return frame
        
        frame_copia = frame.copy()
        for face_landmarks in landmarks:
            for x, y, z in face_landmarks:
                cv2.circle(frame_copia, (x, y), raio, cor, -1)
        
        return frame_copia
    
    def rosto_centralizado(self, frame: np.ndarray, rosto: dict, margem: float = 0.2) -> bool:
        """
        Verifica se um rosto está centralizado no frame.
        
        Args:
            frame: Frame do vídeo
            rosto: Dicionário com informações do rosto
            margem: Margem de tolerância (0.0 a 1.0)
            
        Returns:
            True se o rosto está centralizado, False caso contrário
        """
        h, w = frame.shape[:2]
        
        centro_frame_x = w // 2
        centro_frame_y = h // 2
        
        centro_rosto_x, centro_rosto_y = rosto['centro']
        
        margem_x = w * margem
        margem_y = h * margem
        
        return (abs(centro_frame_x - centro_rosto_x) < margem_x and
                abs(centro_frame_y - centro_rosto_y) < margem_y)
    
    def obter_maior_rosto(self, rostos: list) -> dict:
        """
        Obtém o maior rosto detectado (mais próximo da câmera).
        
        Args:
            rostos: Lista de rostos detectados
            
        Returns:
            Dicionário com o maior rosto
        """
        if not rostos:
            return None
        
        return max(rostos, key=lambda r: r['largura'] * r['altura'])
    
    def calcular_distancia_rosto(self, landmarks: list) -> Optional[float]:
        """
        Calcula uma estimativa de distância do rosto usando landmarks.
        
        Args:
            landmarks: Landmarks de um rosto
            
        Returns:
            Valor de distância estimada
        """
        try:
            if not landmarks or len(landmarks) < 468:
                return None
            
            # Usa a distância entre os olhos como referência
            olho_esquerdo = landmarks[33]  # Olho esquerdo
            olho_direito = landmarks[263]  # Olho direito
            
            distancia = np.sqrt(
                (olho_direito[0] - olho_esquerdo[0])**2 +
                (olho_direito[1] - olho_esquerdo[1])**2
            )
            
            return distancia
        except:
            return None
    
    def __del__(self):
        """Libera recursos ao destruir o objeto."""
        if hasattr(self, 'face_detection'):
            self.face_detection.close()
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()
