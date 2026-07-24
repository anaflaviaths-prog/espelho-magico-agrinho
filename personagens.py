"""
Módulo de Personagens
Gerencia os personagens do Programa Agrinho
"""

import cv2
import numpy as np
from typing import Optional, List, Tuple
from utilitarios import Utilitarios
import os


class Personagem:
    """
    Classe que representa um personagem individual.
    """
    
    def __init__(self, caminho_imagem: str, nome: str = None):
        """
        Inicializa um personagem.
        
        Args:
            caminho_imagem: Caminho da imagem PNG do personagem
            nome: Nome do personagem (opcional)
        """
        self.caminho_imagem = caminho_imagem
        self.nome = nome or os.path.splitext(os.path.basename(caminho_imagem))[0]
        self.imagem = None
        self.largura = 0
        self.altura = 0
        self.x = 0
        self.y = 0
        self.escala = 1.0
        self.rotacao = 0
        self.opacity = 255
        self.animacao_frame = 0
        self.animacao_velocidade = 0
        self.carregada = False
        
        self.carregar()
    
    def carregar(self) -> bool:
        """
        Carrega a imagem do personagem com fundo transparente.
        
        Returns:
            True se carregado com sucesso, False caso contrário
        """
        try:
            if not os.path.exists(self.caminho_imagem):
                print(f"Arquivo não encontrado: {self.caminho_imagem}")
                return False
            
            # Carrega imagem com canal alpha
            self.imagem = cv2.imread(self.caminho_imagem, cv2.IMREAD_UNCHANGED)
            
            if self.imagem is None:
                print(f"Erro ao carregar imagem: {self.caminho_imagem}")
                return False
            
            self.altura, self.largura = self.imagem.shape[:2]
            self.carregada = True
            print(f"Personagem '{self.nome}' carregado com sucesso")
            return True
        
        except Exception as e:
            print(f"Erro ao carregar personagem: {e}")
            return False
    
    def redimensionar(self, escala: float) -> None:
        """
        Redimensiona o personagem.
        
        Args:
            escala: Fator de escala (1.0 = tamanho original)
        """
        self.escala = escala
    
    def posicionar(self, x: int, y: int) -> None:
        """
        Define a posição do personagem.
        
        Args:
            x: Coordenada X
            y: Coordenada Y
        """
        self.x = x
        self.y = y
    
    def rotacionar(self, angulo: float) -> None:
        """
        Define o ângulo de rotação.
        
        Args:
            angulo: Ângulo em graus
        """
        self.rotacao = angulo
    
    def definir_opacity(self, valor: int) -> None:
        """
        Define a opacidade (transparência).
        
        Args:
            valor: Valor de 0 (transparente) a 255 (opaco)
        """
        self.opacity = max(0, min(255, valor))
    
    def animar(self, velocidade: float = 1.0) -> None:
        """
        Anima o personagem.
        
        Args:
            velocidade: Velocidade da animação
        """
        self.animacao_velocidade = velocidade
        self.animacao_frame += velocidade
    
    def obter_imagem_redimensionada(self) -> Optional[np.ndarray]:
        """
        Obtém a imagem redimensionada do personagem.
        
        Returns:
            Imagem redimensionada ou None
        """
        if not self.carregada or self.imagem is None:
            return None
        
        try:
            nova_largura = int(self.largura * self.escala)
            nova_altura = int(self.altura * self.escala)
            
            if nova_largura <= 0 or nova_altura <= 0:
                return None
            
            imagem_redim = cv2.resize(self.imagem, (nova_largura, nova_altura))
            
            # Aplica opacidade
            if self.opacity < 255:
                if imagem_redim.shape[2] == 4:  # RGBA
                    imagem_redim[:, :, 3] = cv2.convertScaleAbs(
                        imagem_redim[:, :, 3],
                        alpha=self.opacity / 255.0
                    )
            
            return imagem_redim
        
        except Exception as e:
            print(f"Erro ao redimensionar personagem: {e}")
            return None


class GerenciadorPersonagens:
    """
    Gerencia múltiplos personagens.
    """
    
    def __init__(self):
        """
        Inicializa o gerenciador de personagens.
        """
        self.personagens = {}
        self.personagens_ativos = []
        self.carregar_personagens_disponiveis()
    
    def carregar_personagens_disponiveis(self) -> None:
        """
        Carrega todos os personagens disponíveis da pasta de personagens.
        """
        caminhos = Utilitarios.listar_personagens()
        
        for caminho in caminhos:
            try:
                nome = os.path.splitext(os.path.basename(caminho))[0]
                personagem = Personagem(caminho, nome)
                if personagem.carregada:
                    self.personagens[nome] = personagem
                    print(f"Personagem '{nome}' registrado")
            except Exception as e:
                print(f"Erro ao carregar personagem {caminho}: {e}")
    
    def obter_personagem(self, nome: str) -> Optional[Personagem]:
        """
        Obtém um personagem pelo nome.
        
        Args:
            nome: Nome do personagem
            
        Returns:
            Objeto Personagem ou None
        """
        return self.personagens.get(nome)
    
    def listar_personagens(self) -> List[str]:
        """
        Lista nomes de todos os personagens disponíveis.
        
        Returns:
            Lista com nomes dos personagens
        """
        return list(self.personagens.keys())
    
    def adicionar_personagem_ativo(self, nome_personagem: str, x: int, y: int, escala: float = 0.3) -> bool:
        """
        Adiciona um personagem aos personagens ativos na tela.
        
        Args:
            nome_personagem: Nome do personagem
            x: Coordenada X
            y: Coordenada Y
            escala: Fator de escala
            
        Returns:
            True se adicionado com sucesso, False caso contrário
        """
        personagem = self.obter_personagem(nome_personagem)
        if personagem is None:
            print(f"Personagem '{nome_personagem}' não encontrado")
            return False
        
        # Cria uma cópia do personagem para uso
        personagem_copia = Personagem(personagem.caminho_imagem, personagem.nome)
        personagem_copia.posicionar(x, y)
        personagem_copia.redimensionar(escala)
        
        self.personagens_ativos.append(personagem_copia)
        return True
    
    def limpar_personagens_ativos(self) -> None:
        """
        Remove todos os personagens ativos.
        """
        self.personagens_ativos.clear()
    
    def desenhar_personagens(self, frame: np.ndarray) -> np.ndarray:
        """
        Desenha todos os personagens ativos no frame.
        
        Args:
            frame: Frame do vídeo
            
        Returns:
            Frame com personagens desenhados
        """
        try:
            frame_resultado = frame.copy()
            
            for personagem in self.personagens_ativos:
                imagem_redim = personagem.obter_imagem_redimensionada()
                if imagem_redim is None:
                    continue
                
                alt_img, larg_img = imagem_redim.shape[:2]
                alt_frame, larg_frame = frame_resultado.shape[:2]
                
                x1 = max(0, personagem.x)
                y1 = max(0, personagem.y)
                x2 = min(larg_frame, personagem.x + larg_img)
                y2 = min(alt_frame, personagem.y + alt_img)
                
                if x1 >= x2 or y1 >= y2:
                    continue
                
                # Define região de origem na imagem
                src_x1 = max(0, -personagem.x)
                src_y1 = max(0, -personagem.y)
                src_x2 = src_x1 + (x2 - x1)
                src_y2 = src_y1 + (y2 - y1)
                
                imagem_cortada = imagem_redim[src_y1:src_y2, src_x1:src_x2]
                
                if imagem_cortada.shape[2] == 4:  # RGBA
                    mascara = imagem_cortada[:, :, 3] / 255.0
                    cores = imagem_cortada[:, :, :3]
                    
                    regiao = frame_resultado[y1:y2, x1:x2]
                    for c in range(3):
                        regiao[:, :, c] = (cores[:, :, c] * mascara +
                                         regiao[:, :, c] * (1 - mascara)).astype(np.uint8)
                    frame_resultado[y1:y2, x1:x2] = regiao
                else:
                    frame_resultado[y1:y2, x1:x2] = imagem_cortada
            
            return frame_resultado
        
        except Exception as e:
            print(f"Erro ao desenhar personagens: {e}")
            return frame
    
    def animar_personagens(self, velocidade: float = 1.0) -> None:
        """
        Anima todos os personagens ativos.
        
        Args:
            velocidade: Velocidade da animação
        """
        for personagem in self.personagens_ativos:
            personagem.animar(velocidade)
