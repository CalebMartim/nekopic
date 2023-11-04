# Bibliotecas principais:

# import tkinter
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from Cliente import Cliente

'''
Definição de classes:
'''


class Imagem(ctk.CTkFrame):
    def __init__(self, master, caminho_arquivo: str, _id: int):
        super().__init__(master)

        # Centraliza a coluna principal
        self.grid_columnconfigure(0, weight=1)

        # Lê e pega as informações do arquivo
        pre_imagem = Image.open(caminho_arquivo)
        tamanho, altura = pre_imagem.size

        # Processa o nome do arquivo
        pre_nome: int = caminho_arquivo.rfind('/')
        if pre_nome != -1:
            pre_nome: str = caminho_arquivo[pre_nome + 1:]
        else:
            pre_nome: str = caminho_arquivo

        # Define a imagem como um objeto CTkImage
        self.imagem = ctk.CTkImage(light_image=pre_imagem, dark_image=pre_imagem,
                                   size=(min(int(tamanho * 0.25), 111), min(int(altura * 0.25), 160)))
        # Passo necessário para deixxar a imagem visível
        self.label = ctk.CTkLabel(self, image=self.imagem, text="")
        self.label.grid(row=0, column=0, pady=(0, 10), columnspan=2)

        # Atributo de nome
        self.nome_label = ctk.CTkLabel(self, text=pre_nome)
        self.nome_label.grid(row=1, column=0, padx=10, pady=5)

        # Atributo de botão de seleção
        self.selecionado = ctk.CTkCheckBox(self, text="", command=self.toggle_selecionar)
        self.selecionado.grid(row=1, column=1, padx=25, pady=5)

        # Atributo de identificador
        self.id = _id

        # Atributo de diretorio
        self.diretorio = caminho_arquivo

        # Atributo de nome
        self.nome = pre_nome

        # Insere a imagem no hashmap de selecionados
        selecionados_complemento.add(self.diretorio)

    def toggle_selecionar(self):
        if self.diretorio in selecionados_complemento:
            selecionados_complemento.remove(self.diretorio)
        else:
            selecionados_complemento.add(self.diretorio)

        if self.nome in selecionados:
            selecionados.remove(self.nome)
        else:
            selecionados.add(self.nome)


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

        # Identificador de cada imagem
        self.id: int = 0

        '''
        Widgets do aplicativo: 
        '''

        # Título princiapl
        header = ctk.CTkLabel(self, text="NEKOPIC")
        header.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        # Botão para deleção de qrquivos
        botao_deletar = ctk.CTkButton(self, text="- Deleter", command=self.deletar_fotos)
        botao_deletar.grid(row=0, column=1, padx=10, pady=10, columnspan=4)

        # Inicialização do quadro de fotos
        self.quadro_fotos = ctk.CTkFrame(self)
        self.quadro_fotos.grid(row=1, column=0, padx=10, pady=(0, 10), columnspan=2)
        # Centraliza as quatro colunas do quadro
        for i in range(4):
            self.quadro_fotos.grid_columnconfigure(i, weight=1)

        # Botão que permite upload de arquivos
        botao_upload_arquivo = ctk.CTkButton(self, text="+ Inserir imagem", command=self.funcao_upload_arquivo)
        botao_upload_arquivo.grid(row=2, column=0, padx=10, pady=10, columnspan=4)

    def funcao_upload_arquivo(self):
        caminho_arquivo: str = filedialog.askopenfilename()

        if caminho_arquivo:
            if cliente.upload(caminho_arquivo):
                imagem = Imagem(self.quadro_fotos, caminho_arquivo, self.id)
                imagem.grid(row=int(self.row_cnt / 4), column=self.col_cnt % 4, pady=(0, 20), padx=10)

                self.row_cnt += 1
                self.col_cnt += 1
                self.id += 1
            else:
                print("Deu ruim")

    def deletar_fotos(self):
        """
        Funciona por refazer o quadro de fotos, adicionando nele
        apenas os elementos que estáo no set 'selecionados_complemento'
        """

        if cliente.delete(selecionados):
            quadro_novo = ctk.CTkFrame(self)

            self.id = 0
            self.row_cnt = 0
            self.col_cnt = 0

            temp_selecionados: set = selecionados_complemento.copy()
            selecionados_complemento.clear()
            selecionados.clear()

            for diretorio in temp_selecionados:
                imagem = Imagem(quadro_novo, diretorio, self.id)
                imagem.grid(row=int(self.row_cnt / 4), column=self.col_cnt % 4, pady=(0, 20), padx=10)

                self.row_cnt += 1
                self.col_cnt += 1
                self.id += 1

            self.quadro_fotos.grid_forget()
            self.quadro_fotos = quadro_novo
            self.quadro_fotos.grid(row=1, column=0, padx=10, pady=(0, 10), columnspan=2)
        else:
            print("Deu ruim")


if __name__ == '__main__':
    '''
    Configurações iniciais e instanciação da classe App:
    '''

    cliente = Cliente()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    # Usamos dois sets para adicionar, remover e verificar itens selecionados em O(1)
    selecionados: set = set()
    selecionados_complemento: set = set()

    app: App = App()
    app.mainloop()
