import wx
import wx.stc
import json
import os

class LimitadorCaracteresApp(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Limitador de Caracteres", size=(600, 650))
        
        # Variáveis principais
        self.texto_antes = ""
        self.texto_depois = ""
        self.pular_espacos = False

        # Criar painel principal
        panel = wx.Panel(self)
        
        # Criar sizer principal
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Área de quantidade de caracteres
        caracteres_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_remover = wx.StaticText(panel, label="Quantidade de caracteres:")
        self.entry_remover = wx.TextCtrl(panel, size=(200, -1))
        caracteres_sizer.Add(label_remover, 0, wx.ALL | wx.CENTER, 5)
        caracteres_sizer.Add(self.entry_remover, 1, wx.ALL | wx.EXPAND, 5)
        
        # Área de texto de entrada
        texto_label = wx.StaticText(panel, label="Insira o texto:")
        self.entry_texto = wx.stc.StyledTextCtrl(panel, size=(580, 150))
        self.entry_texto.SetMarginWidth(1, 0)  # Remove margem de números de linha
        
        # Área de texto de resultado
        resultado_label = wx.StaticText(panel, label="Texto processado:")
        self.entry_resultado = wx.stc.StyledTextCtrl(panel, size=(580, 150))
        self.entry_resultado.SetMarginWidth(1, 0)
        
        # Botões principais
        botoes_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_config = wx.Button(panel, label="Configurar Textos")
        self.btn_processar = wx.Button(panel, label="Processar")
        botoes_sizer.Add(self.btn_config, 0, wx.ALL, 5)
        botoes_sizer.Add(self.btn_processar, 0, wx.ALL, 5)
        
        # Labels de contagem
        self.label_contagem_texto = wx.StaticText(panel, label="Caracteres: 0")
        self.label_contagem_resultado = wx.StaticText(panel, label="Caracteres: 0")
        
        # Adicionar elementos ao sizer principal
        main_sizer.Add(caracteres_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(texto_label, 0, wx.ALL, 5)
        main_sizer.Add(self.entry_texto, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.label_contagem_texto, 0, wx.ALL, 5)
        main_sizer.Add(botoes_sizer, 0, wx.CENTER | wx.ALL, 5)
        main_sizer.Add(resultado_label, 0, wx.ALL, 5)
        main_sizer.Add(self.entry_resultado, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.label_contagem_resultado, 0, wx.ALL, 5)
        
        # Configurar o sizer
        panel.SetSizer(main_sizer)
        
        # Centralizar a janela
        self.Center()
        
        # Bind de eventos
        self.entry_texto.Bind(wx.stc.EVT_STC_CHANGE, self.atualizar_contagem_texto)
        self.entry_resultado.Bind(wx.stc.EVT_STC_CHANGE, self.atualizar_contagem_resultado)
        self.btn_config.Bind(wx.EVT_BUTTON, self.configurar_textos)
        self.btn_processar.Bind(wx.EVT_BUTTON, self.processar_texto)
        
        # Mostrar a janela
        self.Show()

    def atualizar_contagem_texto(self, event):
        texto = self.entry_texto.GetText()
        self.label_contagem_texto.SetLabel(f"Caracteres: {len(texto.strip())}")
        event.Skip()

    def atualizar_contagem_resultado(self, event):
        texto = self.entry_resultado.GetText()
        self.label_contagem_resultado.SetLabel(f"Caracteres: {len(texto.strip())}")
        event.Skip()

    def configurar_textos(self, event):
        # Criar diálogo de configuração
        dialog = wx.Dialog(self, title="Configurar Textos", size=(400, 500))
        dialog_sizer = wx.BoxSizer(wx.VERTICAL)

        # Texto antes
        label_antes = wx.StaticText(dialog, label="Texto antes:")
        entry_antes = wx.stc.StyledTextCtrl(dialog, size=(380, 100))
        entry_antes.SetText(self.texto_antes)
        
        # Texto depois
        label_depois = wx.StaticText(dialog, label="Texto depois:")
        entry_depois = wx.stc.StyledTextCtrl(dialog, size=(380, 100))
        entry_depois.SetText(self.texto_depois)
        
        # Checkbox para pular espaços
        check_espacos = wx.CheckBox(dialog, label="Pular espaços")
        check_espacos.SetValue(self.pular_espacos)
        
        # Botões de preset
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_salvar_preset = wx.Button(dialog, label="Salvar Preset")
        btn_carregar_preset = wx.Button(dialog, label="Carregar Preset")
        btn_sizer.Add(btn_salvar_preset, 0, wx.ALL, 5)
        btn_sizer.Add(btn_carregar_preset, 0, wx.ALL, 5)
        
        # Botões OK/Cancelar
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(dialog, wx.ID_OK, "OK")
        btn_cancel = wx.Button(dialog, wx.ID_CANCEL, "Cancelar")
        button_sizer.Add(btn_ok, 0, wx.ALL, 5)
        button_sizer.Add(btn_cancel, 0, wx.ALL, 5)
        
        # Adicionar elementos ao sizer do diálogo
        dialog_sizer.Add(label_antes, 0, wx.ALL, 5)
        dialog_sizer.Add(entry_antes, 1, wx.EXPAND | wx.ALL, 5)
        dialog_sizer.Add(label_depois, 0, wx.ALL, 5)
        dialog_sizer.Add(entry_depois, 1, wx.EXPAND | wx.ALL, 5)
        dialog_sizer.Add(check_espacos, 0, wx.ALL, 5)
        dialog_sizer.Add(btn_sizer, 0, wx.CENTER | wx.ALL, 5)
        dialog_sizer.Add(button_sizer, 0, wx.CENTER | wx.ALL, 5)
        
        dialog.SetSizer(dialog_sizer)
        
        # Bind eventos dos botões de preset
        btn_salvar_preset.Bind(wx.EVT_BUTTON, 
            lambda evt: self.salvar_preset(entry_antes.GetText(), entry_depois.GetText()))
        btn_carregar_preset.Bind(wx.EVT_BUTTON,
            lambda evt: self.mostrar_presets(entry_antes, entry_depois))
        
        if dialog.ShowModal() == wx.ID_OK:
            self.texto_antes = entry_antes.GetText()
            self.texto_depois = entry_depois.GetText()
            self.pular_espacos = check_espacos.GetValue()
        
        dialog.Destroy()

    def processar_texto(self, event):
        try:
            limite_caracteres = int(self.entry_remover.GetValue())
            texto = self.entry_texto.GetText().strip()
            
            # Considera os textos "antes" e "depois"
            texto_antes = self.texto_antes.rstrip('\n')
            texto_depois = self.texto_depois.lstrip('\n')
            
            # Calcula caracteres disponíveis
            caracteres_antes = len(texto_antes.replace("\n", ""))
            caracteres_depois = len(texto_depois.replace("\n", ""))
            caracteres_disponiveis = limite_caracteres - (caracteres_antes + caracteres_depois)
            
            resultado_final = ""
            if self.pular_espacos:
                # Ignora espaços em excesso
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
            
            self.entry_resultado.SetText(resultado_final)
        except ValueError:
            wx.MessageBox("Por favor, insira um número válido.", "Erro",
                         wx.OK | wx.ICON_ERROR)

    def salvar_preset(self, texto_antes, texto_depois):
        if not os.path.exists("presets"):
            os.makedirs("presets")
        
        # Criar diálogo para nome do preset
        dialog = wx.TextEntryDialog(self, "Nome do preset:", "Salvar Preset")
        
        if dialog.ShowModal() == wx.ID_OK:
            preset_name = dialog.GetValue()
            if preset_name:
                preset_path = f"presets/{preset_name}.json"
                
                # Confirmar sobrescrita se já existir
                if os.path.exists(preset_path):
                    if wx.MessageBox("Preset já existe. Sobrescrever?", "Confirmar",
                                   wx.YES_NO | wx.NO_DEFAULT) != wx.YES:
                        return
                
                # Salvar preset
                preset_data = {
                    "texto_antes": texto_antes,
                    "texto_depois": texto_depois,
                    "pular_espacos": self.pular_espacos
                }
                with open(preset_path, "w") as f:
                    json.dump(preset_data, f)
        
        dialog.Destroy()

    def mostrar_presets(self, entry_antes, entry_depois):
        if not os.path.exists("presets"):
            wx.MessageBox("Nenhum preset encontrado.", "Aviso", wx.OK | wx.ICON_INFORMATION)
            return
        
        # Criar diálogo com lista de presets
        dialog = wx.Dialog(self, title="Carregar Preset", size=(300, 400))
        dialog_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Lista de presets
        list_presets = wx.ListBox(dialog, size=(280, 200))
        for filename in os.listdir("presets"):
            if filename.endswith(".json"):
                list_presets.Append(filename[:-5])
        
        # Botões
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_carregar = wx.Button(dialog, label="Carregar")
        btn_deletar = wx.Button(dialog, label="Deletar")
        btn_sizer.Add(btn_carregar, 0, wx.ALL, 5)
        btn_sizer.Add(btn_deletar, 0, wx.ALL, 5)
        
        dialog_sizer.Add(list_presets, 1, wx.EXPAND | wx.ALL, 5)
        dialog_sizer.Add(btn_sizer, 0, wx.CENTER | wx.ALL, 5)
        
        dialog.SetSizer(dialog_sizer)
        
        # Funções para os botões
        def carregar_preset():
            if list_presets.GetSelection() != wx.NOT_FOUND:
                preset_name = list_presets.GetString(list_presets.GetSelection())
                preset_path = f"presets/{preset_name}.json"
                with open(preset_path, "r") as f:
                    preset_data = json.load(f)
                entry_antes.SetText(preset_data["texto_antes"])
                entry_depois.SetText(preset_data["texto_depois"])
                self.pular_espacos = preset_data["pular_espacos"]
                dialog.Destroy()

        def deletar_preset():
            if list_presets.GetSelection() != wx.NOT_FOUND:
                preset_name = list_presets.GetString(list_presets.GetSelection())
                preset_path = f"presets/{preset_name}.json"
                if wx.MessageBox(f"Tem certeza que deseja deletar o preset '{preset_name}'?", "Confirmar", wx.YES_NO | wx.NO_DEFAULT) == wx.YES:
                    os.remove(preset_path)
                    list_presets.Delete(list_presets.GetSelection())
                    wx.MessageBox("Preset deletado com sucesso!", "Sucesso", wx.OK | wx.ICON_INFORMATION)

        btn_carregar.Bind(wx.EVT_BUTTON, lambda event: carregar_preset())
        btn_deletar.Bind(wx.EVT_BUTTON, lambda event: deletar_preset())

        dialog.ShowModal()
        dialog.Destroy()

if __name__ == "__main__":
    app = wx.App(False)
    frame = LimitadorCaracteresApp()
    app.MainLoop()