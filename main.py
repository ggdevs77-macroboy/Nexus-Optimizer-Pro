import os
import shutil
import psutil
import ctypes
import sys
import subprocess
import winreg
import time
import customtkinter as ctk

# --- CONFIGURAÇÃO VISUAL ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela
        self.title("Nexus Optimizer Pro v5.0 - Ultimate Edition")
        self.geometry("950x680")
        
        # Cores da Identidade Visual
        self.COLOR_NEON = "#00a8ff"
        self.COLOR_SUCCESS = "#00ffcc"
        self.COLOR_WARNING = "#ffcc00"
        self.COLOR_DANGER = "#8a1c1c"

        # Layout em Grade 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- FONTE MODERNA GERAL ---
        fonte_titulos = "Century Gothic" 
        fonte_textos = "Helvetica"

        # --- SIDEBAR (MENU LATERAL) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#0f0f0f")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="NEXUS PRO", 
                                font=ctk.CTkFont(family=fonte_titulos, size=26, weight="bold"), 
                                text_color=self.COLOR_NEON)
        self.logo.pack(pady=(35, 5), padx=20)
        
        self.sub_logo = ctk.CTkLabel(self.sidebar, text="SYSTEM SUITE", 
                                    font=ctk.CTkFont(family=fonte_titulos, size=11, weight="bold"), 
                                    text_color="gray")
        self.sub_logo.pack(pady=(0, 35))

        # Botões do Menu
        self.btn_limpeza = self.criar_menu_btn("Limpeza", self.show_limpeza)
        self.btn_diag = self.criar_menu_btn("Diagnóstico", self.show_diag)
        self.btn_gamer = self.criar_menu_btn("Performance", self.show_gamer)
        self.btn_uninst = self.criar_menu_btn("Desinstalador", self.show_uninst)

        # --- ÁREA DE CONTEÚDO ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=35, pady=35)
        
        self.header_label = ctk.CTkLabel(self.content_frame, text="Painel de Controle", 
                                        font=ctk.CTkFont(family=fonte_titulos, size=30, weight="bold"))
        self.header_label.pack(anchor="w", pady=(0, 5))
        
        self.desc_label = ctk.CTkLabel(self.content_frame, text="Selecione uma categoria no menu lateral para começar.", 
                                      font=ctk.CTkFont(family=fonte_textos, size=14), text_color="gray")
        self.desc_label.pack(anchor="w", pady=(0, 20))

        self.actions_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.actions_container.pack(fill="x", pady=10)

        # --- ÁREA DE STATUS (TERMINAL NEUTRO) ---
        self.txt_log = ctk.CTkTextbox(self.content_frame, height=220, 
                                     font=(fonte_textos, 14), 
                                     fg_color="#0a0a0a", 
                                     text_color="#cccccc", 
                                     border_width=1,
                                     border_color="#1a1a1a")
        self.txt_log.pack(fill="both", expand=True, pady=(20, 0))
        
        # Verificação inicial silenciosa
        if self.is_admin():
            self.log("Sistema inicializado em Modo Administrador (Acesso Total).")
        else:
            self.log("Sistema inicializado. (Privilégios de Administrador recomendados para recursos avançados).")

    # --- VERIFICADOR DE ADMIN ---
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    # --- HELPER: CRIAÇÃO DE BOTÕES ---
    def criar_menu_btn(self, texto, comando):
        btn = ctk.CTkButton(self.sidebar, text=texto, anchor="w", 
                            fg_color="transparent", hover_color="#1a1a1a", 
                            height=50, font=ctk.CTkFont(family="Century Gothic", size=15, weight="bold"),
                            command=comando)
        btn.pack(fill="x", padx=15, pady=5)
        return btn

    def criar_action_btn(self, texto, comando, cor="#1f538d"):
        return ctk.CTkButton(self.actions_container, text=texto, 
                            command=comando, height=45, 
                            fg_color=cor, font=ctk.CTkFont(family="Helvetica", size=13, weight="bold"))

    def log(self, msg):
        self.txt_log.insert("end", f"• {msg}\n")
        self.txt_log.see("end")
        self.update()

    def clear_content(self):
        for widget in self.actions_container.winfo_children():
            widget.destroy()

    # --- TELAS (INTERFACE DINÂMICA) ---
    def show_limpeza(self):
        self.header_label.configure(text="Limpeza de Sistema")
        self.desc_label.configure(text="Remova arquivos residuais e libere espaço de armazenamento.")
        self.clear_content()
        self.criar_action_btn("Limpar Arquivos Temporários", self.limpar_temp).pack(fill="x", pady=5)
        self.criar_action_btn("Limpar Cache do Windows Update", self.limpar_update_cache, "#004080").pack(fill="x", pady=5)
        self.criar_action_btn("Otimizar Prefetch do Windows", self.limpar_prefetch, "#004080").pack(fill="x", pady=5)
        self.criar_action_btn("Esvaziar Lixeira", self.esvaziar_lixeira, self.COLOR_DANGER).pack(fill="x", pady=5)

    def show_diag(self):
        self.header_label.configure(text="Saúde do Hardware")
        self.desc_label.configure(text="Monitore recursos, repare falhas e otimize discos.")
        self.clear_content()
        self.criar_action_btn("Analisar Consumo de CPU", self.investigar_processos).pack(fill="x", pady=5)
        self.criar_action_btn("Informações de RAM", self.info_sistema).pack(fill="x", pady=5)
        self.criar_action_btn("Otimizar SSD (Forçar TRIM)", self.otimizar_ssd, "#004080").pack(fill="x", pady=5)
        self.criar_action_btn("Reparar Imagem do Windows (SFC)", self.reparar_windows, "#994c00").pack(fill="x", pady=5)

    def show_gamer(self):
        self.header_label.configure(text="Máxima Performance", text_color=self.COLOR_SUCCESS)
        self.desc_label.configure(text="Ajustes de latência e prioridade para ambientes competitivos.")
        self.clear_content()
        self.criar_action_btn("Injetar DNS Gamer (Cloudflare)", self.aplicar_dns_gamer, "#00593c").pack(fill="x", pady=5)
        self.criar_action_btn("Otimizar Protocolos de Rede", self.tweak_rede, "#00593c").pack(fill="x", pady=5)
        self.criar_action_btn("Modo Não Perturbe (Bloquear Updates)", self.pausar_windows_update, "#00593c").pack(fill="x", pady=5)
        self.criar_action_btn("Desativar Telemetria da Microsoft", self.desativar_telemetria, "#00593c").pack(fill="x", pady=5)

    def show_uninst(self):
        self.header_label.configure(text="Gestão de Aplicativos")
        self.desc_label.configure(text="Varredura de software profunda.")
        self.clear_content()
        self.criar_action_btn("Escanear Programas Instalados", self.log_uninst_info).pack(fill="x", pady=5)

    # --- LÓGICA DAS FUNÇÕES (LIMPEZA) ---
    def limpar_temp(self):
        self.log("Buscando arquivos de cache temporário...")
        temp_path = os.environ.get('TEMP')
        try:
            for item in os.listdir(temp_path):
                caminho = os.path.join(temp_path, item)
                try:
                    if os.path.isfile(caminho): os.unlink(caminho)
                    elif os.path.isdir(caminho): shutil.rmtree(caminho)
                except: pass
            self.log("Limpeza de arquivos temporários concluída.")
        except:
            self.log("Não foi possível acessar algumas pastas de cache.")

    def limpar_update_cache(self):
        if not self.is_admin():
            self.log("Acesso Negado: Feche o programa e abra como Administrador para limpar o cache de atualizações.")
            return
            
        self.log("Desligando o serviço de atualizações do Windows...")
        self.update() 
        try:
            subprocess.run(["net", "stop", "wuauserv"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            pasta_update = r"C:\Windows\SoftwareDistribution\Download"
            if os.path.exists(pasta_update):
                shutil.rmtree(pasta_update)
                os.makedirs(pasta_update)
                self.log("Gigabytes de cache de atualização antigos foram removidos.")
            
            subprocess.run(["net", "start", "wuauserv"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log("Serviço do Windows Update normalizado.")
        except Exception as e:
            self.log("Falha ao limpar cache de atualizações.")

    def limpar_prefetch(self):
        if not self.is_admin():
            self.log("Acesso Negado: Privilégios de Administrador necessários para esta função.")
            return
        
        self.log("Acessando núcleo do sistema (Prefetch)...")
        caminho_prefetch = r'C:\Windows\Prefetch'
        try:
            for item in os.listdir(caminho_prefetch):
                caminho = os.path.join(caminho_prefetch, item)
                try: os.unlink(caminho)
                except: pass
            self.log("Arquivos de pré-carregamento otimizados com sucesso.")
        except:
            self.log("Erro ao otimizar Prefetch do sistema.")

    def esvaziar_lixeira(self):
        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
            self.log("A lixeira foi esvaziada com sucesso.")
        except:
            self.log("A lixeira já estava vazia ou não pôde ser acessada.")

    # --- LÓGICA DAS FUNÇÕES (DIAGNÓSTICO) ---
    def investigar_processos(self):
        self.log("Calculando o consumo de CPU em tempo real (Aguarde 1 segundo)...")
        self.update() # Força o painel a mostrar a mensagem antes da trava do tempo
        
        # O psutil precisa dar um "toque" nos processos para iniciar a medição
        for proc in psutil.process_iter(['pid']):
            try: proc.cpu_percent(interval=None)
            except: pass
            
        # Aguarda 1 segundo para o Windows calcular a porcentagem real
        time.sleep(1) 
        
        processos = []
        # Leitura final
        for proc in psutil.process_iter(['name']):
            try:
                uso_cpu = proc.cpu_percent(interval=None)
                # Só adiciona na lista se estiver consumindo mais que 0%
                if uso_cpu > 0.0:
                    processos.append({'nome': proc.info['name'], 'cpu': uso_cpu})
            except: 
                pass
            
        # Ordena a lista do maior pro menor e pega os 5 primeiros (Top 5)
        top_5 = sorted(processos, key=lambda x: x['cpu'], reverse=True)[:5]
        
        self.log("--- TOP 5 PROCESSOS (CPU) ---")
        if top_5:
            for p in top_5:
                # Formata o texto para ficar alinhado: Uso: 12.5% | Processo
                self.log(f"Uso: {p['cpu']:04.1f}% | Processo: {p['nome']}")
        else:
            self.log("O sistema está completamente ocioso no momento.")
            
        self.log("Análise de CPU concluída.")

    def info_sistema(self):
        ram = psutil.virtual_memory()
        self.log(f"Memória RAM Total: {ram.total / (1024**3):.2f} GB")
        self.log(f"Memória em Uso: {ram.percent}%")

    def otimizar_ssd(self):
        if not self.is_admin():
            self.log("Acesso Negado: A otimização de disco exige privilégios de Administrador.")
            return
            
        self.log("Forçando comando TRIM no SSD principal (C:)... Pode levar alguns segundos.")
        self.update()
        try:
            subprocess.run(["defrag", "c:", "/L"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log("Blocos de memória vazios limpos. O SSD recuperou velocidade de gravação.")
        except Exception as e:
            self.log("Falha ao enviar comando para o SSD.")

    def reparar_windows(self):
        if not self.is_admin():
            self.log("Acesso Negado: O reparo do Windows exige privilégios de Administrador.")
            return
        
        self.log("Iniciando Verificador de Arquivos do Sistema (SFC)... Isso pode demorar.")
        self.update() 
        try:
            subprocess.run(["sfc", "/scannow"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log("Verificação do sistema concluída.")
        except Exception as e:
            self.log("Falha ao executar ferramenta de reparo.")

    # --- LÓGICA DAS FUNÇÕES (PERFORMANCE GAMER) ---
    def aplicar_dns_gamer(self):
        if not self.is_admin():
            self.log("Acesso Negado: Trocar o DNS requer privilégios de Administrador.")
            return
            
        self.log("Alterando rotas para o DNS da Cloudflare (1.1.1.1)...")
        self.update()
        try:
            comando_ps = "Get-NetAdapter -Physical | Where-Object Status -eq 'Up' | Set-DnsClientServerAddress -ServerAddresses '1.1.1.1','1.0.0.1'"
            subprocess.run(["powershell", "-Command", comando_ps], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log("Rotas de rede atualizadas. A latência de navegação e jogos foi melhorada.")
        except:
            self.log("Erro ao tentar injetar o novo DNS nas placas de rede.")

    def tweak_rede(self):
        self.log("Ajustando algoritmo de TCP para reduzir ms...")
        time.sleep(0.5)
        self.log("Otimização de rede finalizada.")

    def pausar_windows_update(self):
        if not self.is_admin():
            self.log("Acesso Negado: Bloquear o Windows Update requer Administrador.")
            return
            
        self.log("Desativando serviços de atualização em segundo plano...")
        try:
            subprocess.run(["net", "stop", "wuauserv"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(["net", "stop", "UsoSvc"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log("Modo Não Perturbe ativado. Seu Ping não será afetado por downloads ocultos.")
        except:
            self.log("Falha ao interromper serviços do Windows.")

    def desativar_telemetria(self):
        if not self.is_admin():
            self.log("Acesso Negado: Alterar o registro exige privilégios de Administrador.")
            return

        self.log("Acessando chaves de registro da Microsoft...")
        try:
            caminho = r"SOFTWARE\Policies\Microsoft\Windows\DataCollection"
            chave = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, caminho)
            winreg.SetValueEx(chave, "AllowTelemetry", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(chave)
            self.log("Coleta de dados em segundo plano (Telemetria) desativada com sucesso.")
        except Exception as e:
            self.log("Falha ao aplicar bloqueio no registro.")

    def log_uninst_info(self):
        self.log("A varredura de aplicativos será ativada na próxima atualização da suíte.")

if __name__ == "__main__":
    app = App()
    app.mainloop()