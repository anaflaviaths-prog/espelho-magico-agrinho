"""
Módulo de Interface
Interface gráfica do Espelho Mágico Agrinho usando CustomTkinter
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import time
from typing import Optional

from camera import Camera
from detector import Detector
from personagens import GerenciadorPersonagens
from cenarios import GerenciadorCenarios
from efeitos import GerenciadorEfeitos
from captura import Captura
from moldura import Moldura
from som import GerenciadorSom
from configuracoes import config
from utilitarios import Utilitarios


class Interface:
    """
    Interface gráfica do aplicativo.
    """
    
    def __init__(self):
        """
        Inicializa a interface.
        """
        # Configura tema
        ctk.set_appearance_mode("dark" if config.obter("modo_escuro", True) else "light")
        ctk.set_default_color_theme("green")
        
        # Cria janela principal
        self.janela = ctk.CTk()
        self.janela.title("🌾 Espelho Mágico Agrinho - Feira Agrinho 2026")
        self.janela.geometry("1280x800")
        
        # Modo fullscreen
        if config.obter("fullscreen", True):
            self.janela.attributes('-fullscreen', True)
        
        # Inicializa componentes
        self.camera = None
        self.detector = Detector()
        self.gerenciador_personagens = GerenciadorPersonagens()
        self.gerenciador_cenarios = GerenciadorCenarios()
        self.gerenciador_efeitos = GerenciadorEfeitos()
        self.captura = Captura()
        self.gerenciador_som = GerenciadorSom()
        
        # Estados
        self.rodando = False
        self.capturando = False
        self.contagem_regressiva = 0
        self.tempo_contagem = config.obter("tempo_contagem", 3)
        self.rosto_detectado = False
        self.rosto_centralizado = False
        
        # Thread para captura de vídeo
        self.thread_video = None
        
        # Cria a interface
        self.criar_interface()
    
    def criar_interface(self) -> None:
        """
        Cria os elementos da interface.
        """
        # Frame principal com gradiente de cores tema Agrinho
        self.frame_principal = ctk.CTkFrame(self.janela, fg_color=(34, 139, 34))
        self.frame_principal.pack(fill="both", expand=True)
        
        # Título
        titulo = ctk.CTkLabel(
            self.frame_principal,
            text="🌾 Espelho Mágico Agrinho 🌾",
            font=("Arial", 36, "bold"),
            text_color="white"
        )
        titulo.pack(pady=20)
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            self.frame_principal,
            text="Feira Agrinho 2026 - Escola Municipal Prefeito Durval Wolff do Amaral",
            font=("Arial", 14),
            text_color="#FFFF99"
        )
        subtitulo.pack(pady=5)
        
        # Frame de conteúdo
        frame_conteudo = ctk.CTkFrame(self.frame_principal, fg_color=(34, 139, 34))
        frame_conteudo.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Frame para vídeo
        self.frame_video = ctk.CTkLabel(
            frame_conteudo,
            text="Preparando câmera...",
            font=("Arial", 20),
            fg_color=(50, 50, 50),
            width=800,
            height=600
        )
        self.frame_video.pack(side="left", padx=20, pady=20)
        
        # Frame de controles
        frame_controles = ctk.CTkFrame(frame_conteudo, fg_color=(34, 139, 34))
        frame_controles.pack(side="right", fill="both", expand=True, padx=20)
        
        # Botão Iniciar
        self.btn_iniciar = ctk.CTkButton(
            frame_controles,
            text="😋 Iniciar",
            font=("Arial", 18, "bold"),
            fg_color=(0, 200, 0),
            hover_color=(0, 150, 0),
            height=50,
            command=self.iniciar_captura
        )
        self.btn_iniciar.pack(pady=10, fill="x")
        
        # Botão Parar
        self.btn_parar = ctk.CTkButton(
            frame_controles,
            text="⛔ Parar",
            font=("Arial", 18, "bold"),
            fg_color=(200, 0, 0),
            hover_color=(150, 0, 0),
            height=50,
            command=self.parar_captura,
            state="disabled"
        )
        self.btn_parar.pack(pady=10, fill="x")
        
        # Botão Capturar Foto
        self.btn_capturar = ctk.CTkButton(
            frame_controles,
            text="📷 Capturar Foto",
            font=("Arial", 18, "bold"),
            fg_color=(0, 100, 200),
            hover_color=(0, 50, 150),
            height=50,
            command=self.capturar_foto,
            state="disabled"
        )
        self.btn_capturar.pack(pady=10, fill="x")
        
        # Label para status
        self.label_status = ctk.CTkLabel(
            frame_controles,
            text="Status: Inativo",
            font=("Arial", 12),
            text_color="white"
        )
        self.label_status.pack(pady=10, fill="x")
        
        # Label para dicas
        self.label_dicas = ctk.CTkLabel(
            frame_controles,
            text="Posicione-se frente \u00e0 c\u00e2mera",
            font=("Arial", 11),
            text_color="#FFFF99"
        )
        self.label_dicas.pack(pady=10, fill="x")
        
        # Divisor
        ctk.CTkLabel(frame_controles, text="", fg_color="white", height=2).pack(pady=10, fill="x")
        
        # Seção de Configurações
        label_config = ctk.CTkLabel(
            frame_controles,
            text="\u2699️ Configurações",
            font=("Arial", 14, "bold"),
            text_color="white"
        )
        label_config.pack(pady=10)
        
        # Switch de Efeitos
        self.switch_efeitos = ctk.CTkSwitch(
            frame_controles,
            text="Efeitos Visuais",
            onvalue=True,
            offvalue=False,
            command=self.alternar_efeitos,
            text_color="white"
        )
        self.switch_efeitos.pack(pady=5, fill="x")
        self.switch_efeitos.select() if config.obter("efeitos_visuais", True) else self.switch_efeitos.deselect()
        
        # Switch de Sons
        self.switch_sons = ctk.CTkSwitch(
            frame_controles,
            text="Sons",
            onvalue=True,
            offvalue=False,
            command=self.alternar_sons,
            text_color="white"
        )
        self.switch_sons.pack(pady=5, fill="x")
        self.switch_sons.select() if config.obter("sons", True) else self.switch_sons.deselect()
        
        # Botão Sair
        self.btn_sair = ctk.CTkButton(
            frame_controles,
            text="❌ Sair",
            font=("Arial", 14, "bold"),
            fg_color=(100, 0, 0),
            hover_color=(150, 0, 0),
            height=40,
            command=self.sair
        )
        self.btn_sair.pack(pady=20, fill="x", side="bottom")
    
    def iniciar_captura(self) -> None:
        """
        Inicia a captura de vídeo.
        """
        try:
            self.camera = Camera()
            if not self.camera.conectar():
                messagebox.showerror("Erro", "Não foi possível acessar a câmera")
                return
            
            self.rodando = True
            self.btn_iniciar.configure(state="disabled")
            self.btn_parar.configure(state="normal")
            self.btn_capturar.configure(state="normal")
            self.label_status.configure(text="Status: Câmera Ativa")
            
            # Inicia thread de vídeo
            self.thread_video = threading.Thread(target=self.loop_video, daemon=True)
            self.thread_video.start()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar: {e}")
    
    def parar_captura(self) -> None:
        """
        Para a captura de vídeo.
        """
        self.rodando = False
        self.capturando = False
        
        if self.camera:
            self.camera.desconectar()
        
        self.btn_iniciar.configure(state="normal")
        self.btn_parar.configure(state="disabled")
        self.btn_capturar.configure(state="disabled")
        self.label_status.configure(text="Status: Inativo")
        self.label_dicas.configure(text="Posicione-se frente \u00e0 c\u00e2mera")
        
        # Mostra imagem padrao
        self.frame_video.configure(text="C\u00e2mera Desconectada", image=None)
    
    def loop_video(self) -> None:
        """
        Loop principal de vídeo.
        """
        while self.rodando:
            try:
                frame = self.camera.capturar_frame()
                if frame is None:
                    continue
                
                # Espelha o frame
                frame = self.camera.espelhar_horizontalmente(frame)
                
                # Detecta rostos
                rostos = self.detector.detectar_rostos(frame)
                
                if rostos:
                    self.rosto_detectado = True
                    maior_rosto = self.detector.obter_maior_rosto(rostos)
                    
                    # Desenha caixa do rosto
                    frame = self.detector.desenhar_caixa_rosto(frame, [maior_rosto], cor=(0, 255, 0))
                    
                    # Verifica se está centralizado
                    self.rosto_centralizado = self.detector.rosto_centralizado(frame, maior_rosto)
                    
                    if self.rosto_centralizado:
                        self.label_dicas.configure(text="✅ Rosto Centralizado! Prepare-se para capturar.")
                    else:
                        self.label_dicas.configure(text="Centralize seu rosto")
                else:
                    self.rosto_detectado = False
                    self.label_dicas.configure(text="Nenhum rosto detectado")
                
                # Adiciona efeitos
                if config.obter("efeitos_visuais", True):
                    self.gerenciador_efeitos.desenhar(frame)
                    self.gerenciador_efeitos.atualizar()
                
                # Adiciona personagens
                if config.obter("personagens", True) and rostos:
                    self.gerenciador_personagens.limpar_personagens_ativos()
                    personagens = self.gerenciador_personagens.listar_personagens()
                    
                    if personagens:
                        # Adiciona personagens aos lados
                        for i, nome_personagem in enumerate(personagens[:2]):
                            x = 50 + (i * 250)
                            y = 100
                            self.gerenciador_personagens.adicionar_personagem_ativo(nome_personagem, x, y, 0.4)
                    
                    frame = self.gerenciador_personagens.desenhar_personagens(frame)
                
                # Converte para RGB para exibir
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Redimensiona para exibir
                frame_redim = Utilitarios.redimensionar_imagem(frame_rgb, 800, 600)
                
                # Converte para PhotoImage
                imagem_pil = Image.fromarray(frame_redim)
                imagem_tk = ImageTk.PhotoImage(imagem_pil)
                
                # Atualiza label com imagem
                self.frame_video.configure(image=imagem_tk, text="")
                self.frame_video.image = imagem_tk
                
                # Processos de captura
                if self.capturando:
                    self.processar_captura(frame)
                
                time.sleep(0.03)  # ~30 FPS
            
            except Exception as e:
                print(f"Erro no loop de vídeo: {e}")
                break
    
    def capturar_foto(self) -> None:
        """
        Inicia o processo de captura de foto.
        """
        if not self.rosto_detectado:
            messagebox.showwarning("Aviso", "Nenhum rosto detectado")
            return
        
        self.capturando = True
        self.contagem_regressiva = self.tempo_contagem
        self.label_dicas.configure(text="Contagem regressiva...")
    
    def processar_captura(self, frame: np.ndarray) -> None:
        """
        Processa o frame durante a contagem regressiva.
        
        Args:
            frame: Frame atual
        """
        if self.contagem_regressiva > 0:
            self.label_dicas.configure(text=f"Capturando em {self.contagem_regressiva}...")
            self.gerenciador_som.reproduzir_som('click') if 'click' in self.gerenciador_som.sons else None
            self.contagem_regressiva -= 1
        else:
            # Captura a foto
            self.captura.capturar_frame(frame)
            caminho = self.captura.salvar_foto()
            
            if caminho:
                # Aplica moldura
                moldura = Moldura(1000, 700)
                frame_moldura = moldura.criar_moldura_agrinho(frame)
                
                # Salva com moldura
                cv2.imwrite(caminho.replace('.png', '_moldura.png'), frame_moldura)
                
                self.label_dicas.configure(text="✅ Foto capturada com sucesso!")
                self.gerenciador_som.reproduzir_som('foto') if 'foto' in self.gerenciador_som.sons else None
                messagebox.showinfo("Sucesso", f"Foto salva em:\n{caminho}")
            
            self.capturando = False
    
    def alternar_efeitos(self) -> None:
        """
        Alterna os efeitos visuais.
        """
        ativo = self.switch_efeitos.get()
        config.definir("efeitos_visuais", ativo)
    
    def alternar_sons(self) -> None:
        """
        Alterna os sons.
        """
        ativo = self.switch_sons.get()
        config.definir("sons", ativo)
        self.gerenciador_som.habilitar_sons(ativo)
    
    def sair(self) -> None:
        """
        Fecha o aplicativo.
        """
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.rodando = False
            if self.camera:
                self.camera.desconectar()
            self.janela.quit()
            self.janela.destroy()
    
    def executar(self) -> None:
        """
        Executa a interface.
        """
        self.janela.mainloop()
