# Bibliotecas principais:

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from Cliente import Cliente

'''
Definição de classes:
'''


class JanelaSucesso(ctk.CTkToplevel):
    def __init__(self, *args):
        super().__init__(*args)

        self.geometry("250x125")
        self.grid_columnconfigure(0, weight=1)

        self.title("Ok!")

        self.label = ctk.CTkLabel(self, text="Foto(s) baixada(s) com sucesso")
        self.button = ctk.CTkButton(self, text="ok", fg_color="#4b80ca", command=self.dispensar)

        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.button.grid(row=1, column=0, padx=10, pady=10)

    def dispensar(self):
        self.destroy()


class JanelaFalha(ctk.CTkToplevel):
    def __init__(self, *args, arquivos):
        super().__init__(*args)

        self.geometry("200x200")
        self.grid_columnconfigure(0, weight=1)

        self.title("Ops!")
        falha = "Falhas nos seguintes arquivos:\n"

        for arquivo in arquivos:
            falha += arquivo + '\n'

        self.label = ctk.CTkLabel(self, text=falha)
        self.button = ctk.CTkButton(self, text="ok", fg_color="#4b80ca", command=self.dispensar)

        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.button.grid(row=1, column=0, padx=10, pady=10)

    def dispensar(self):
        self.destroy()


class Imagem(ctk.CTkFrame):
    def __init__(self, master, nome: str, imagem_pil):
        super().__init__(master)

        # Centraliza a coluna principal
        self.grid_columnconfigure(0, weight=1)

        # Lê e pega as informações do arquivo
        self.imagem_pil = imagem_pil

        tamanho, altura = self.imagem_pil.size

        # Define a imagem como um objeto CTkImage
        self.imagem_ctk = ctk.CTkImage(light_image=self.imagem_pil, dark_image=self.imagem_pil,
                                       size=(min(int(tamanho * 0.25), 111), min(int(altura * 0.25), 160)))

        # Passo necessário para deixar a imagem visível
        self.label = ctk.CTkLabel(self, image=self.imagem_ctk, text="")
        self.label.grid(row=0, column=0, pady=(0, 10), columnspan=2)

        # Atributo de nome
        self.nome_label = ctk.CTkLabel(self, text=nome)
        self.nome_label.grid(row=1, column=0, padx=10, pady=5)

        # Atributo de botão de seleção
        self.selecionado = ctk.CTkCheckBox(self, text="", command=self.toggle_selecionar)
        self.selecionado.grid(row=1, column=1, padx=25, pady=5)

        # Atributo de nome
        self.nome = nome

        # Insere a imagem no hashmap de selecionados
        selecionados_complemento[self.nome] = self.imagem_pil

    def toggle_selecionar(self):
        if self.nome in selecionados_complemento:
            selecionados_complemento.pop(self.nome)
        else:
            selecionados_complemento[self.nome] = self.imagem_pil

        if self.nome in selecionados:
            selecionados.pop(self.nome)
        else:
            selecionados[self.nome] = self.imagem_pil


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("720x480")
        self.title("NEKOPIC")

        # Centraliza os itens da primeira coluna
        self.grid_columnconfigure(0, weight=1)

        '''
        Variáveis auxiliares:
        '''
        # Contador de linhas e colunas para auxiliar o posicionamento das imagens
        self.row_cnt: int = 0
        self.col_cnt: int = 0

        '''
        Widgets do aplicativo: 
        '''

        # Título princiapl
        header = ctk.CTkLabel(self, text="NEKOPIC")
        header.grid(row=0, column=0, padx=10, pady=10)

        # Botão para baixar de qrquivos
        botao_download_arquivo = ctk.CTkButton(self, text="Baixar", command=self.baixar_fotos, fg_color="#4b80ca")
        botao_download_arquivo.grid(row=0, column=1, padx=10, pady=10)

        # Botão para deleção de qrquivos
        botao_deletar_arquivo = ctk.CTkButton(self, text="- Deletar", command=self.deletar_fotos, fg_color="#b45252")
        botao_deletar_arquivo.grid(row=0, column=2, padx=10, pady=10)

        # Inicialização do quadro de fotos
        self.quadro_fotos = ctk.CTkFrame(self)
        self.quadro_fotos.grid(row=1, column=0, padx=10, pady=(0, 10), columnspan=3)

        # Centraliza as quatro colunas do quadro
        for i in range(4):
            self.quadro_fotos.grid_columnconfigure(i, weight=1)

        # Insere as fotos iniciais encontradas no servidor
        for (nome, imagem) in cliente.imagens():
            self.insere_no_quadro(nome, imagem)

        # Botão que permite upload de arquivos
        botao_upload_arquivo = ctk.CTkButton(self, text="+ Inserir imagem", command=self.funcao_upload_arquivo)
        botao_upload_arquivo.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

        self.toplevel_window = None

    def insere_no_quadro(self, nome: str, img):
        imagem = Imagem(self.quadro_fotos, nome, img)
        imagem.grid(row=int(self.row_cnt / 4), column=self.col_cnt % 4, pady=(0, 20), padx=10)

        self.row_cnt += 1
        self.col_cnt += 1

    def funcao_upload_arquivo(self):
        caminho_arquivo: str = filedialog.askopenfilename()
        if caminho_arquivo:
            nome: int = caminho_arquivo.rfind('/')
            if nome != -1:
                nome: str = caminho_arquivo[nome + 1:]
            else:
                nome: str = caminho_arquivo

            if caminho_arquivo:
                if cliente.upload(caminho_arquivo):
                    self.insere_no_quadro(nome, Image.open(caminho_arquivo))
                else:
                    self.toplevel_window = JanelaFalha(self, arquivos=[nome])

    def deletar_fotos(self):
        """
        Funciona por refazer o quadro de fotos, adicionando nele
        apenas os elementos que estáo no set 'selecionados_complemento'
        """
        if selecionados:
            resultado = cliente.delete(selecionados)
            if resultado[0]:
                quadro_novo = ctk.CTkFrame(self)

                self.row_cnt = 0
                self.col_cnt = 0

                temp_selecionados: dict = selecionados_complemento.copy()
                selecionados_complemento.clear()
                selecionados.clear()

                for nome, img in temp_selecionados.items():
                    imagem = Imagem(quadro_novo, nome, img)
                    imagem.grid(row=int(self.row_cnt / 4), column=self.col_cnt % 4, pady=(0, 20), padx=10)

                    self.row_cnt += 1
                    self.col_cnt += 1

                self.quadro_fotos.grid_forget()
                self.quadro_fotos = quadro_novo
                self.quadro_fotos.grid(row=1, column=0, padx=10, pady=(0, 10), columnspan=3)
            else:
                self.toplevel_window = JanelaFalha(self, arquivos=resultado[1])

    def baixar_fotos(self):
        diretorio = filedialog.askdirectory()
        resultado = cliente.download(selecionados, diretorio)
        if diretorio:
            if resultado[0]:
                self.toplevel_window = JanelaSucesso(self)
            else:
                self.toplevel_window = JanelaFalha(self, arquivos=resultado[1])


if __name__ == '__main__':
    '''
    Configurações iniciais e instanciação da classe App:
    '''

    cliente = Cliente()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    # Usamos dois sets para adicionar, remover e verificar itens selecionados em O(1)
    selecionados: dict = dict()
    selecionados_complemento: dict = dict()

    app: App = App()
    app.mainloop()
