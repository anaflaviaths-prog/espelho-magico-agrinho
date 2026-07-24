"""
Módulo de Efeitos Visuais
Gerencia efeitos visuais como partículas, animações, etc
"""

import cv2
import numpy as np
import random
from typing import List, Tuple


class Particula:
    """
    Classe que representa uma partícula para efeitos.
    """
    
    def __init__(self, x: float, y: float, vx: float, vy: float, cor: Tuple, tamanho: int = 5, vida: int = 100):
        """
        Inicializa uma partícula.
        
        Args:
            x: Posição X inicial
            y: Posição Y inicial
            vx: Velocidade X
            vy: Velocidade Y
            cor: Cor em BGR
            tamanho: Tamanho da partícula
            vida: Tempo de vida em frames
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.cor = cor
        self.tamanho = tamanho
        self.vida_maxima = vida
        self.vida = vida
        self.ativa = True
    
    def atualizar(self) -> None:
        """
        Atualiza a posição e vida da partícula.
        """
        self.x += self.vx
        self.y += self.vy
        self.vida -= 1
        
        # Aplica gravidade
        self.vy += 0.1
        
        if self.vida <= 0:
            self.ativa = False
    
    def desenhar(self, frame: np.ndarray) -> None:
        """
        Desenha a partícula no frame.
        
        Args:
            frame: Frame do vídeo
        """
        if not self.ativa:
            return
        
        x = int(self.x)
        y = int(self.y)
        
        # Verifica se está dentro dos limites do frame
        if x < 0 or x >= frame.shape[1] or y < 0 or y >= frame.shape[0]:
            return
        
        # Opacidade baseada na vida restante
        alfa = self.vida / self.vida_maxima
        
        # Desenha círculo com opacidade
        tamanho_atual = int(self.tamanho * alfa)
        if tamanho_atual > 0:
            cv2.circle(frame, (x, y), tamanho_atual, self.cor, -1)


class EmissorParticulas:
    """
    Classe que emite e gerencia partículas.
    """
    
    def __init__(self):
        """
        Inicializa o emissor de partículas.
        """
        self.particulas = []
    
    def emitir_folhas_caindo(self, x: int, y: int, quantidade: int = 5) -> None:
        """
        Emite partículas simulating folhas caindo.
        
        Args:
            x: Posição X
            y: Posição Y
            quantidade: Quantidade de folhas
        """
        for _ in range(quantidade):
            vx = random.uniform(-1, 1)
            vy = random.uniform(0.5, 2)
            cor = (0, random.randint(100, 255), 0)  # Verde variado
            self.particulas.append(Particula(x, y, vx, vy, cor, tamanho=8, vida=200))
    
    def emitir_sementes(self, x: int, y: int, quantidade: int = 5) -> None:
        """
        Emite partículas representando sementes.
        
        Args:
            x: Posição X
            y: Posição Y
            quantidade: Quantidade de sementes
        """
        for _ in range(quantidade):
            vx = random.uniform(-2, 2)
            vy = random.uniform(-2, 1)
            cor = (139, 69, 19)  # Marrom
            self.particulas.append(Particula(x, y, vx, vy, cor, tamanho=4, vida=150))
    
    def emitir_flores(self, x: int, y: int, quantidade: int = 3) -> None:
        """
        Emite partículas representando flores.
        
        Args:
            x: Posição X
            y: Posição Y
            quantidade: Quantidade de flores
        """
        for _ in range(quantidade):
            vx = random.uniform(-1, 1)
            vy = random.uniform(-1, 1)
            cores_flores = [(0, 0, 255), (255, 0, 0), (0, 255, 255), (255, 0, 255)]  # Vermelho, azul, ciano, magenta
            cor = random.choice(cores_flores)
            self.particulas.append(Particula(x, y, vx, vy, cor, tamanho=6, vida=180))
    
    def emitir_brilho(self, x: int, y: int, quantidade: int = 10) -> None:
        """
        Emite partículas de brilho.
        
        Args:
            x: Posição X
            y: Posição Y
            quantidade: Quantidade de partículas
        """
        for _ in range(quantidade):
            vx = random.uniform(-1.5, 1.5)
            vy = random.uniform(-1.5, 1.5)
            cor = (255, 255, 255)  # Branco
            self.particulas.append(Particula(x, y, vx, vy, cor, tamanho=3, vida=100))
    
    def atualizar(self) -> None:
        """
        Atualiza todas as partículas.
        """
        for particula in self.particulas:
            particula.atualizar()
        
        # Remove partículas inativas
        self.particulas = [p for p in self.particulas if p.ativa]
    
    def desenhar_todas(self, frame: np.ndarray) -> None:
        """
        Desenha todas as partículas.
        
        Args:
            frame: Frame do vídeo
        """
        for particula in self.particulas:
            particula.desenhar(frame)
    
    def limpar(self) -> None:
        """
        Remove todas as partículas.
        """
        self.particulas.clear()


class GerenciadorEfeitos:
    """
    Gerencia todos os efeitos visuais.
    """
    
    def __init__(self):
        """
        Inicializa o gerenciador de efeitos.
        """
        self.emissor = EmissorParticulas()
        self.efeitos_habilitados = {
            'folhas': True,
            'sementes': True,
            'flores': True,
            'brilho': True
        }
    
    def habilitar_efeito(self, nome_efeito: str, ativo: bool = True) -> None:
        """
        Habilita ou desabilita um efeito.
        
        Args:
            nome_efeito: Nome do efeito
            ativo: True para habilitar, False para desabilitar
        """
        if nome_efeito in self.efeitos_habilitados:
            self.efeitos_habilitados[nome_efeito] = ativo
    
    def acionar_efeito(self, nome_efeito: str, x: int, y: int, quantidade: int = 5) -> None:
        """
        Aciona um efeito específico.
        
        Args:
            nome_efeito: Nome do efeito ('folhas', 'sementes', 'flores', 'brilho')
            x: Posição X
            y: Posição Y
            quantidade: Quantidade de partículas
        """
        if not self.efeitos_habilitados.get(nome_efeito, True):
            return
        
        if nome_efeito == 'folhas':
            self.emissor.emitir_folhas_caindo(x, y, quantidade)
        elif nome_efeito == 'sementes':
            self.emissor.emitir_sementes(x, y, quantidade)
        elif nome_efeito == 'flores':
            self.emissor.emitir_flores(x, y, quantidade)
        elif nome_efeito == 'brilho':
            self.emissor.emitir_brilho(x, y, quantidade)
    
    def atualizar(self) -> None:
        """
        Atualiza todos os efeitos.
        """
        self.emissor.atualizar()
    
    def desenhar(self, frame: np.ndarray) -> None:
        """
        Desenha todos os efeitos no frame.
        
        Args:
            frame: Frame do vídeo
        """
        self.emissor.desenhar_todas(frame)
    
    def limpar(self) -> None:
        """
        Remove todos os efeitos.
        """
        self.emissor.limpar()
