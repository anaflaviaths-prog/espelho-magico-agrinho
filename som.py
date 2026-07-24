"""
Módulo de Som
Gerencia efeitos sonoros e música do aplicativo
"""

import pygame
import os
from typing import Optional
from utilitarios import Utilitarios
from configuracoes import config


class GerenciadorSom:
    """
    Classe para gerenciar sons e música.
    """
    
    def __init__(self):
        """
        Inicializa o gerenciador de som.
        """
        try:
            pygame.mixer.init()
            self.sons = {}
            self.volume = config.obter('volume', 70) / 100.0
            self.sons_habilitados = config.obter('sons', True)
            self.carregador_sons()
        except Exception as e:
            print(f"Aviso: Não foi possível inicializar áudio: {e}")
    
    def carregador_sons(self) -> None:
        """
        Carrega todos os sons disponíveis.
        """
        sons_dict = Utilitarios.listar_sons()
        
        for nome, caminho in sons_dict.items():
            try:
                som = pygame.mixer.Sound(caminho)
                som.set_volume(self.volume)
                self.sons[nome] = som
                print(f"Som '{nome}' carregado")
            except Exception as e:
                print(f"Erro ao carregar som {nome}: {e}")
    
    def reproduzir_som(self, nome_som: str) -> bool:
        """
        Reproduz um som.
        
        Args:
            nome_som: Nome do som a reproduzir
            
        Returns:
            True se reproduzido, False caso contrário
        """
        if not self.sons_habilitados:
            return False
        
        if nome_som not in self.sons:
            print(f"Som '{nome_som}' não encontrado")
            return False
        
        try:
            self.sons[nome_som].play()
            return True
        except Exception as e:
            print(f"Erro ao reproduzir som: {e}")
            return False
    
    def parar_som(self, nome_som: str) -> bool:
        """
        Para a reprodução de um som.
        
        Args:
            nome_som: Nome do som a parar
            
        Returns:
            True se parado, False caso contrário
        """
        if nome_som not in self.sons:
            return False
        
        try:
            self.sons[nome_som].stop()
            return True
        except:
            return False
    
    def definir_volume(self, volume: float) -> None:
        """
        Define o volume para todos os sons.
        
        Args:
            volume: Volume de 0.0 a 1.0
        """
        self.volume = max(0.0, min(1.0, volume))
        for som in self.sons.values():
            som.set_volume(self.volume)
    
    def habilitar_sons(self, ativo: bool) -> None:
        """
        Habilita ou desabilita sons.
        
        Args:
            ativo: True para habilitar, False para desabilitar
        """
        self.sons_habilitados = ativo
    
    def parar_todos(self) -> None:
        """
        Para todos os sons em reprodução.
        """
        pygame.mixer.stop()
    
    def __del__(self):
        """Limpa recursos ao destruir o objeto."""
        try:
            pygame.mixer.quit()
        except:
            pass
