import tkinter as tk
from tkinter import ttk

class LimitadorCaracteresApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Limitador de Caracteres")
        self.root.geometry("600x650")

        # Variáveis para armazenar os textos antes e depois
        self.texto_antes = ""
        self.texto_depois = ""
        self.pular_espacos = tk.BooleanVar()

        # Rótulo e campo para informar a quantidade de caracteres
        label_remover = ttk.Label(self.root, text="Quantidade de caracteres:")
        label_remover.pack(pady=5)
        self.entry_remover = ttk.Entry(self.root, width=70)
        self.entry_remover.pack(pady=5)

        # Rótulo e campo para inserir o texto a ser processado com barra de rolagem
        label_texto = ttk.Label(self.root, text="Insira o texto:")
        label_texto.pack(pady=5)
        frame_texto = ttk.Frame(self.root)
        frame_texto.pack(pady=5)

        scroll_texto = tk.Scrollbar(frame_texto)
        scroll_texto.pack(side=tk.RIGHT, fill=tk.Y)
        self.entry_texto = tk.Text(frame_texto, height=10, width=70, yscrollcommand=scroll_texto.set)
        self.entry_texto.pack(side=tk.LEFT, fill=tk.BOTH)
        scroll_texto.config(command=self.entry_texto.yview)

        # Botões para o campo de entrada de texto
        frame_botoes_texto = ttk.Frame(self.root)
        frame_botoes_texto.pack(pady=5)
        ttk.Button(frame_botoes_texto, text="Copiar", command=lambda: self.copiar(self.entry_texto)).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botoes_texto, text="Colar", command=lambda: self.colar(self.entry_texto)).grid(row=0, column=1, padx=5)
        ttk.Button(frame_botoes_texto, text="Selecionar Tudo", command=lambda: self.selecionar_tudo(self.entry_texto)).grid(row=0, column=2, padx=5)
        ttk.Button(frame_botoes_texto, text="Limpar", command=lambda: self.limpar(self.entry_texto)).grid(row=0, column=3, padx=5)

        # Botão "Configurar Textos"
        ttk.Button(self.root, text="Configurar Textos", command=self.configurar_textos).pack(pady=10)

        # Botão "Processar"
        ttk.Button(self.root, text="Processar", command=self.processar_texto).pack(pady=10)

        # Rótulo e campo para mostrar o texto processado com barra de rolagem
        label_resultado = ttk.Label(self.root, text="Texto processado:")
        label_resultado.pack(pady=5)
        frame_resultado = ttk.Frame(self.root)
        frame_resultado.pack(pady=5)

        scroll_resultado = tk.Scrollbar(frame_resultado)
        scroll_resultado.pack(side=tk.RIGHT, fill=tk.Y)
        self.entry_resultado = tk.Text(frame_resultado, height=10, width=70, yscrollcommand=scroll_resultado.set)
        self.entry_resultado.pack(side=tk.LEFT, fill=tk.BOTH)
        scroll_resultado.config(command=self.entry_resultado.yview)

        # Botões para o campo de texto processado
        frame_botoes_resultado = ttk.Frame(self.root)
        frame_botoes_resultado.pack(pady=5)
        ttk.Button(frame_botoes_resultado, text="Copiar", command=lambda: self.copiar(self.entry_resultado)).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botoes_resultado, text="Colar", command=lambda: self.colar(self.entry_resultado)).grid(row=0, column=1, padx=5)
        ttk.Button(frame_botoes_resultado, text="Selecionar Tudo", command=lambda: self.selecionar_tudo(self.entry_resultado)).grid(row=0, column=2, padx=5)
        ttk.Button(frame_botoes_resultado, text="Limpar", command=lambda: self.limpar(self.entry_resultado)).grid(row=0, column=3, padx=5)

    # Função para processar o texto
    def processar_texto(self):
        try:
            limite_caracteres = int(self.entry_remover.get())
            texto = self.entry_texto.get("1.0", tk.END).strip()

            # Considera os textos "antes" e "depois", mantendo suas quebras de linha
            texto_antes = self.texto_antes.rstrip('\n')
            texto_depois = self.texto_depois.lstrip('\n')

            # Calcular quantos caracteres podem ser utilizados para o texto principal
            caracteres_antes = len(texto_antes.replace("\n", ""))
            caracteres_depois = len(texto_depois.replace("\n", ""))
            caracteres_disponiveis = limite_caracteres - (caracteres_antes + caracteres_depois)

            # Variável para armazenar o resultado final
            resultado_final = ""

            if self.pular_espacos.get():
                # Ignora espaços em excesso, mas mantém um espaço simples entre palavras
                i = 0
                while i < len(texto):
                    texto_temp = ""
                    while len(texto_temp) < caracteres_disponiveis and i < len(texto):
                        if texto[i] != ' ' or (texto_temp and texto_temp[-1] != ' '):
                            texto_temp += texto[i]
                        i += 1
                    resultado_final += texto_antes + texto_temp + texto_depois + "\n"
            else:
                texto_processado = texto[:caracteres_disponiveis]
                resultado_final = texto_antes + texto_processado + texto_depois

            self.entry_resultado.delete("1.0", tk.END)
            self.entry_resultado.insert(tk.END, resultado_final)
        except ValueError:
            self.entry_resultado.delete("1.0", tk.END)
            self.entry_resultado.insert(tk.END, "Por favor, insira um número válido.")

    # Função para configurar os textos antes e depois
    def configurar_textos(self):
        janela_config = tk.Toplevel(self.root)
        janela_config.title("Configurar Textos")
        janela_config.geometry("400x350")

        label_antes = ttk.Label(janela_config, text="Texto antes:")
        label_antes.pack(pady=5)
        entry_antes = tk.Text(janela_config, height=5, width=50)
        entry_antes.pack(pady=5)
        entry_antes.insert("1.0", self.texto_antes)

        label_depois = ttk.Label(janela_config, text="Texto depois:")
        label_depois.pack(pady=5)
        entry_depois = tk.Text(janela_config, height=5, width=50)
        entry_depois.pack(pady=5)
        entry_depois.insert("1.0", self.texto_depois)

        check_box = ttk.Checkbutton(janela_config, text="Pular espaços", variable=self.pular_espacos)
        check_box.pack(pady=10)

        def salvar_textos():
            self.texto_antes = entry_antes.get("1.0", tk.END).rstrip() + "\n"
            self.texto_depois = entry_depois.get("1.0", tk.END).rstrip() + "\n"
            janela_config.destroy()

        botao_salvar = ttk.Button(janela_config, text="Salvar", command=salvar_textos)
        botao_salvar.pack(pady=10)

    # Funções para copiar, colar, selecionar tudo e limpar
    def copiar(self, widget):
        widget.event_generate("<<Copy>>")

    def colar(self, widget):
        widget.event_generate("<<Paste>>")

    def selecionar_tudo(self, widget):
        widget.tag_add("sel", "1.0", "end")
        widget.mark_set("insert", "1.0")
        widget.see("insert")
        widget.focus()

    def limpar(self, widget):
        widget.delete("1.0", tk.END)

# Inicializando a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = LimitadorCaracteresApp(root)
    root.mainloop()
