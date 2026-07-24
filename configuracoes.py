"""
Módulo de Configurações
Gerencia as configurações do aplicativo Espelho Mágico Agrinho
"""

import json
import os
from pathlib import Path
from typing import Any, Dict


class Configuracoes:
    """
    Classe para gerenciar as configurações do aplicativo.
    Armazena e recupera configurações em um arquivo JSON.
    """
    
    def __init__(self, arquivo_config: str = "config.json"):
        """
        Inicializa o gerenciador de configurações.
        
        Args:
            arquivo_config: Caminho do arquivo de configuração
        """
        self.arquivo_config = arquivo_config
        self.configuracoes_padrao = {
            "camera": 0,
            "resolucao": "1280x720",
            "tempo_contagem": 3,
            "efeitos_visuais": True,
            "musica": True,
            "sons": True,
            "brilho": 1.0,
            "contraste": 1.0,
            "cenario_padrao": "fazenda",
            "personagens": True,
            "animacoes": True,
            "volume": 70,
            "fullscreen": True,
            "pixelacao": False,
            "modo_escuro": True,
        }
        self.configuracoes = self.carregar()
    
    def carregar(self) -> Dict[str, Any]:
        """
        Carrega as configurações do arquivo JSON.
        Se o arquivo não existir, cria com as configurações padrão.
        
        Returns:
            Dicionário com as configurações
        """
        if os.path.exists(self.arquivo_config):
            try:
                with open(self.arquivo_config, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Mescla com padrão para garantir todas as chaves
                    return {**self.configuracoes_padrao, **config}
            except (json.JSONDecodeError, IOError) as e:
                print(f"Erro ao carregar configurações: {e}")
                return self.configuracoes_padrao.copy()
        else:
            self.salvar()
            return self.configuracoes_padrao.copy()
    
    def salvar(self) -> None:
        """Salva as configurações atuais no arquivo JSON."""
        try:
            with open(self.arquivo_config, 'w', encoding='utf-8') as f:
                json.dump(self.configuracoes, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Erro ao salvar configurações: {e}")
    
    def obter(self, chave: str, padrao: Any = None) -> Any:
        """
        Obtém o valor de uma configuração.
        
        Args:
            chave: Nome da configuração
            padrao: Valor padrão se a chave não existir
            
        Returns:
            Valor da configuração ou padrão
        """
        return self.configuracoes.get(chave, padrao)
    
    def definir(self, chave: str, valor: Any) -> None:
        """
        Define o valor de uma configuração.
        
        Args:
            chave: Nome da configuração
            valor: Novo valor
        """
        self.configuracoes[chave] = valor
        self.salvar()
    
    def atualizar(self, novas_config: Dict[str, Any]) -> None:
        """
        Atualiza múltiplas configurações de uma vez.
        
        Args:
            novas_config: Dicionário com as configurações a atualizar
        """
        self.configuracoes.update(novas_config)
        self.salvar()
    
    def resetar_padrao(self) -> None:
        """Reseta todas as configurações para o padrão."""
        self.configuracoes = self.configuracoes_padrao.copy()
        self.salvar()
    
    def __str__(self) -> str:
        """Retorna representação em string das configurações."""
        return json.dumps(self.configuracoes, indent=4, ensure_ascii=False)


# Instância global de configurações
config = Configuracoes()
