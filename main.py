# Bibliotecas principais:

import customtkinter as ctk
import time
import threading
from tkinter import filedialog
from PIL import Image
from Cliente import Cliente

'''
Definição de classes:
'''


class Imagem(ctk.CTkFrame):
    def __init__(self, master, nome: str, imagem_pil, pre_selecionado: bool = False):
        super().__init__(master)

        # Imagem em si
        self.imagem_pil = imagem_pil

        tamanho, altura = self.imagem_pil.size

        # Define a imagem como um objeto CTkImage
        self.imagem_ctk = ctk.CTkImage(light_image=self.imagem_pil, dark_image=self.imagem_pil,
                                       size=(min(int(tamanho * 0.25), 111), min(int(altura * 0.25), 160)))

        # Passo necessário para deixar a imagem visível
        self.label = ctk.CTkLabel(self, image=self.imagem_ctk, text="")
        self.label.grid(row=0, column=0, pady=(0, 10), columnspan=3)

        # Atributo de botão de renomear
        self.renomear = ctk.CTkButton(self, text="Renomear", command=self.editar_nome, width=10,
                                      fg_color="#45444f")

        # Atributo de nome visível
        self.nome_label = ctk.CTkLabel(self, text=nome.split('.')[0])

        # Atributo de botão de seleção
        self.selecionado = ctk.CTkCheckBox(self, text="", command=self.toggle_selecionar)

        # Atributo do nome em si
        self.nome = nome

        if pre_selecionado:
            self.selecionado.select()
        else:
            selecionados_complemento[self.nome] = self.imagem_pil

        self.renomear.grid(row=1, column=0, pady=5, padx=10)
        self.nome_label.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.selecionado.grid(row=1, column=2, pady=5)

    def toggle_selecionar(self):
        if self.nome in selecionados_complemento:
            selecionados_complemento.pop(self.nome)
        else:
            selecionados_complemento[self.nome] = self.imagem_pil

        if self.nome in selecionados:
            selecionados.pop(self.nome)
        else:
            selecionados[self.nome] = self.imagem_pil

    def editar_nome(self):
        """
        Edita o nome de algum arquivo, mantendo a sua extensão
        """

        global pause
        pause = True
        dialog = ctk.CTkInputDialog(text="Digite o novo nome: ", title=self.nome)
        text = dialog.get_input()

        if text:
            if cliente.renomear(self.nome, text):
                self.nome_label.forget()
                self.nome_label = ctk.CTkLabel(self, text=text)
                self.nome_label.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

                novo_nome = text + '.' + self.nome.split('.')[-1]

                if self.nome in selecionados:
                    selecionados.pop(self.nome)
                    selecionados[novo_nome] = self.imagem_pil

                if self.nome in selecionados_complemento:
                    selecionados_complemento.pop(self.nome)
                    selecionados_complemento[novo_nome] = self.imagem_pil

                self.nome = novo_nome
            else:
                app.toplevel_window = JanelaFalha(app, arquivos=[self.nome])
        pause = False


class Quadro(ctk.CTkScrollableFrame):
    def __init__(self, master, values):
        super().__init__(master)

        # Centraliza as colunas
        self.grid_columnconfigure(0, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        # Parâmetros para a inserção de imagens novas no quadro
        self.row: int = 0
        self.col: int = 0

        # Insere os itens iniciais
        for value in values:
            self.inserir(value[0], value[1])

    def inserir(self, nome, img):
        """
        Faz a imagem aparecer de fato
        """

        imagem = Imagem(self, nome, img, nome in selecionados)
        imagem.grid(row=int(self.row / 4), column=self.col % 4, pady=(0, 20), padx=10)

        self.row += 1
        self.col += 1


class JanelaSucesso(ctk.CTkToplevel):
    def __init__(self, *args):
        super().__init__(*args)

        # Define tamanho da janela e centraliza conteúdo
        self.geometry("250x125")
        self.grid_columnconfigure(0, weight=1)

        # Título da janela
        self.title("Ok!")

        '''
        Widgets da janela
        '''
        self.label = ctk.CTkLabel(self, text="Foto(s) baixada(s) com sucesso")
        self.button = ctk.CTkButton(self, text="Ok", fg_color="#4b80ca", command=self.dispensar)

        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.button.grid(row=1, column=0, padx=10, pady=10)

    def dispensar(self):
        self.destroy()


class JanelaFalha(ctk.CTkToplevel):
    def __init__(self, *args, arquivos):
        super().__init__(*args)

        # Define tamanho da janela e centraliza conteúdo
        self.geometry("200x200")
        self.grid_columnconfigure(0, weight=1)

        # Título da janela
        self.title("Ops!")

        # Especifica onde falhou
        falha = "Falha nos seguintes arquivos:\n"
        for arquivo in arquivos:
            falha += arquivo + '\n'

        self.label = ctk.CTkLabel(self, text=falha)
        self.button = ctk.CTkButton(self, text="Ok", fg_color="#4b80ca", command=self.dispensar)

        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.button.grid(row=1, column=0, padx=10, pady=10)

    def dispensar(self):
        self.destroy()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Tamanho da janela e título da janela
        self.geometry("720x480")
        self.title("NEKOPIC")

        # Centraliza os itens da primeira coluna
        # e faz a linha do quadro ocupar a tela
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        '''
        Widgets do aplicativo: 
        '''

        # Título principal
        header = ctk.CTkLabel(self, text="NEKOPIC")
        header.grid(row=0, column=0, padx=10, pady=10)

        # Botão para baixar arquivos
        botao_download_arquivo = ctk.CTkButton(self, text="↓ Baixar", command=self.baixar_fotos, fg_color="#4b80ca")
        botao_download_arquivo.grid(row=0, column=1, padx=10, pady=10)

        # Botão para deleção de qrquivos
        botao_deletar_arquivo = ctk.CTkButton(self, text="- Deletar", command=self.deletar_fotos, fg_color="#b45252")
        botao_deletar_arquivo.grid(row=0, column=2, padx=10, pady=10)

        # Botão que permite upload de arquivos
        botao_upload_arquivo = ctk.CTkButton(self, text="+ Inserir imagem", command=self.funcao_upload_arquivo)
        botao_upload_arquivo.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

        # Inicialmente, nenhuma janela sobrepõe a principal
        self.toplevel_window = None

        # Insere as fotos iniciais encontradas no servidor
        fotos_iniciais = []
        for (nome, imagem) in cliente.imagens():
            fotos_iniciais.append([nome, imagem])

        # Inicialização do quadro de fotos
        self.quadro_fotos = Quadro(self, fotos_iniciais)
        self.quadro_fotos.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

    def funcao_upload_arquivo(self):
        """
        Pergunta do usuário o caminho para um arquivo,
        pega o nome do arquivo e insere no quadro de fotos
        """
        caminho_arquivos: str = filedialog.askopenfilenames()

        if caminho_arquivos:
            for caminho_arquivo in caminho_arquivos:
                nome: int = caminho_arquivo.rfind('/')
                if nome != -1:
                    nome: str = caminho_arquivo[nome + 1:]
                else:
                    nome: str = caminho_arquivo

                if cliente.upload(caminho_arquivo):
                    self.quadro_fotos.inserir(nome, Image.open(caminho_arquivo))
                else:
                    self.toplevel_window = JanelaFalha(self, arquivos=[nome])

    def deletar_fotos(self):
        """
        Funciona por refazer o quadro de fotos, adicionando nele
        apenas os elementos que estáo no dicionário 'selecionados_complemento'
        """
        if selecionados:
            resultado = cliente.delete(selecionados)
            if resultado[0]:
                temp_selecionados: dict = selecionados_complemento.copy()
                selecionados_complemento.clear()
                selecionados.clear()

                novos = []
                for nome, img in temp_selecionados.items():
                    novos.append([nome, img])

                self.quadro_fotos.forget()
                self.quadro_fotos = Quadro(self, novos)
                self.quadro_fotos.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")
            else:
                self.toplevel_window = JanelaFalha(self, arquivos=resultado[1])

    def baixar_fotos(self):
        diretorio = filedialog.askdirectory()
        if diretorio:
            resultado = cliente.download(selecionados, diretorio)
            if resultado[0]:
                self.toplevel_window = JanelaSucesso(self)
            else:
                self.toplevel_window = JanelaFalha(self, arquivos=resultado[1])


def atualizar():
    """
    Atualiza a interface gráfica de 10 em 10 segundos
    """

    global pare
    global pause

    while not pare:
        if not pause:
            novos = []
            for nome, img in cliente.imagens():
                novos.append([nome, img])
            selecionados_complemento.clear()
            app.quadro_fotos.forget()
            app.quadro_fotos = Quadro(app, novos)
            app.quadro_fotos.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

        time.sleep(10)


if __name__ == '__main__':
    '''
    Configurações iniciais e instanciação da classe App:
    '''

    cliente = Cliente()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    # Usamos dois dicionários para adicionar, remover e verificar itens selecionados em O(1)
    selecionados: dict = dict()
    selecionados_complemento: dict = dict()

    app: App = App()

    # Parâmetro para pausar ou parar completamente a thread de atualização
    pause = False
    pare = False

    # Utilizamos multi_threading para atualizar em "tempo real" a interface gráfica
    thread = threading.Thread(target=atualizar)
    thread.start()

    app.mainloop()

    # Para a thread de atualização quando a janela é fechada
    pare = not pare

    thread.join()
