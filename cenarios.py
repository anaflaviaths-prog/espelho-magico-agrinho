"""
Módulo de Cenários
Gerencia os cenários de fundo do aplicativo
"""

import cv2
import numpy as np
from typing import Optional, List
from utilitarios import Utilitarios
import os


class Cenario:
    """
    Classe que representa um cenário de fundo.
    """
    
    def __init__(self, caminho_imagem: str, nome: str = None):
        """
        Inicializa um cenário.
        
        Args:
            caminho_imagem: Caminho da imagem do cenário
            nome: Nome do cenário (opcional)
        """
        self.caminho_imagem = caminho_imagem
        self.nome = nome or os.path.splitext(os.path.basename(caminho_imagem))[0]
        self.imagem = None
        self.imagem_redim = None
        self.largura = 0
        self.altura = 0
        self.carregada = False
        
        self.carregar()
    
    def carregar(self) -> bool:
        """
        Carrega a imagem do cenário.
        
        Returns:
            True se carregada com sucesso, False caso contrário
        """
        try:
            if not os.path.exists(self.caminho_imagem):
                print(f"Arquivo não encontrado: {self.caminho_imagem}")
                return False
            
            self.imagem = cv2.imread(self.caminho_imagem)
            
            if self.imagem is None:
                print(f"Erro ao carregar cenário: {self.caminho_imagem}")
                return False
            
            self.altura, self.largura = self.imagem.shape[:2]
            self.carregada = True
            print(f"Cenário '{self.nome}' carregado com sucesso")
            return True
        
        except Exception as e:
            print(f"Erro ao carregar cenário: {e}")
            return False
    
    def redimensionar(self, largura: int, altura: int) -> np.ndarray:
        """
        Redimensiona o cenário para as dimensões especificadas.
        
        Args:
            largura: Largura desejada
            altura: Altura desejada
            
        Returns:
            Imagem redimensionada
        """
        if self.imagem is None:
            return None
        
        try:
            self.imagem_redim = cv2.resize(self.imagem, (largura, altura), interpolation=cv2.INTER_AREA)
            return self.imagem_redim
        
        except Exception as e:
            print(f"Erro ao redimensionar cenário: {e}")
            return None
    
    def obter_imagem_redimensionada(self, largura: int, altura: int) -> Optional[np.ndarray]:
        """
        Obtém a imagem redimensionada.
        
        Args:
            largura: Largura desejada
            altura: Altura desejada
            
        Returns:
            Imagem redimensionada
        """
        return self.redimensionar(largura, altura)


class GerenciadorCenarios:
    """
    Gerencia os cenários disponíveis.
    """
    
    def __init__(self):
        """
        Inicializa o gerenciador de cenários.
        """
        self.cenarios = {}
        self.cenario_ativo = None
        self.carregar_cenarios_disponiveis()
    
    def carregar_cenarios_disponiveis(self) -> None:
        """
        Carrega todos os cenários disponíveis da pasta de cenários.
        """
        caminhos = Utilitarios.listar_cenarios()
        
        for caminho in caminhos:
            try:
                nome = os.path.splitext(os.path.basename(caminho))[0]
                cenario = Cenario(caminho, nome)
                if cenario.carregada:
                    self.cenarios[nome] = cenario
                    print(f"Cenário '{nome}' registrado")
            except Exception as e:
                print(f"Erro ao carregar cenário {caminho}: {e}")
    
    def obter_cenario(self, nome: str) -> Optional[Cenario]:
        """
        Obtém um cenário pelo nome.
        
        Args:
            nome: Nome do cenário
            
        Returns:
            Objeto Cenario ou None
        """
        return self.cenarios.get(nome)
    
    def listar_cenarios(self) -> List[str]:
        """
        Lista nomes de todos os cenários disponíveis.
        
        Returns:
            Lista com nomes dos cenários
        """
        return list(self.cenarios.keys())
    
    def definir_cenario_ativo(self, nome: str) -> bool:
        """
        Define qual cenário está ativo.
        
        Args:
            nome: Nome do cenário
            
        Returns:
            True se definido com sucesso, False caso contrário
        """
        cenario = self.obter_cenario(nome)
        if cenario is None:
            print(f"Cenário '{nome}' não encontrado")
            return False
        
        self.cenario_ativo = cenario
        print(f"Cenário ativo: {nome}")
        return True
    
    def obter_cenario_redimensionado(self, largura: int, altura: int) -> Optional[np.ndarray]:
        """
        Obtém o cenário ativo redimensionado.
        
        Args:
            largura: Largura desejada
            altura: Altura desejada
            
        Returns:
            Imagem do cenário redimensionada
        """
        if self.cenario_ativo is None:
            # Cria imagem vazia se nenhum cenário está ativo
            return np.ones((altura, largura, 3), dtype=np.uint8) * 255
        
        return self.cenario_ativo.obter_imagem_redimensionada(largura, altura)
