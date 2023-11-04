# Bibliotecas principais:

# import tkinter
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image


'''
Definição de classes:
'''


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("720x480")
        self.title("NEKOPIC")

        # Centraliza os itens da primeira coluna
        self.grid_columnconfigure(0, weight=1)

        '''
        Widgets do aplicativo: 
        '''

        # Título princiapl
        header = ctk.CTkLabel(self, text="NEKOPIC")
        header.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        # Botão que permite upload de arquivos
        botao_upload_arquivo = ctk.CTkButton(self, text="+ Inserir imagem", command=self.funcao_upload_arquivo)
        botao_upload_arquivo.grid(row=2, column=0, padx=10, pady=10, columnspan=4)

        # Inicialização do quadro de fotos
        self.quadro_fotos = ctk.CTkFrame(self)
        self.quadro_fotos.grid(row=1, column=0, padx=10, pady=(0, 10))

        # Centraliza as quatro colunas do quadro
        for i in range(4):
            self.quadro_fotos.grid_columnconfigure(i, weight=1)

        # Contador de linhas e colunas para auxiliar o posicionamento das imagens
        self.row_cnt = 0
        self.col_cnt = 0

    def funcao_upload_arquivo(self):
        arquivo_caminho = filedialog.askopenfilename()

        if arquivo_caminho:
            imagem = Image.open(arquivo_caminho)
            tamanho, altura = imagem.size

            pre_nome = arquivo_caminho.rfind('/')

            if pre_nome != -1:
                nome = arquivo_caminho[pre_nome + 1:]
            else:
                nome = arquivo_caminho

            imagem_ctk = ctk.CTkImage(light_image=imagem, dark_image=imagem,
                                      size=(min(int(tamanho*0.25), 111), min(int(altura*0.25), 160)))

            label = ctk.CTkLabel(self.quadro_fotos, image=imagem_ctk, text="")

            if not(self.row_cnt % 4) and self.row_cnt > 0:
                self.row_cnt += 4

            label.grid(row=int(self.row_cnt/4), column=self.col_cnt % 4, pady=(0, 20), padx=10)

            nome_imagem = ctk.CTkLabel(self.quadro_fotos, text=nome)
            nome_imagem.grid(row=int(self.row_cnt/4) + 1, column=self.col_cnt % 4, pady=(0, 10), padx=10)

            self.row_cnt += 1
            self.col_cnt += 1


if __name__ == '__main__':

    '''
    Configurações iniciais e instanciação da classe App:
    '''

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    app = App()
    app.mainloop()
