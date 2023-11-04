# bibliotecas essenciais
import ftplib
import os

class Servidor:
    def __init__(self,host,user,password, wd = None):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__wd = wd

        # inicia o servidor com um timeout de 30s,
        # isto e, ha um tempo de espera de no maximo
        # 30s para se conectar no servidor antes de ser removido
        self.__ftp = ftplib.FTP_TLS(timeout = 30)

    # retorna o objeto FTP
    def get_ftp(self):
        return self.__ftp
    
    # retorna uma lista dos arquivos presentes no diretorio de trabalho atual do servidor
    def get_files(self):
        return self.__ftp.nlst()

    # conecta no servidor dado host
    def connect(self):
        self.__ftp.connect(host=self.__host)

    # login no servidor dado user e senha
    def login(self):
        self.__ftp.login(user=self.__user,passwd=self.__password)

    # estabelece um conexao segura (servidor FTP_TLS)
    def secure_data_connection(self):
        self.__ftp.prot_p()

    # sai do servidor
    def quit(self):
        self.__ftp.quit()

    # define um novo diretorio de trabalho atual
    def set_wd(self, new_wd):
        try:
            if new_wd == self.__wd: return

            self.__wd = new_wd
            self.__ftp.cwd(self.__wd)

        except ftplib.error_perm as e:
            print(f"Erro: {e}")
            return
    
    # retorna o nome do arquivo dependendo do OS
    def __get_arquivo(arquivo):
        # linux
        if "/" in arquivo:
            return arquivo.split("/")[-1]
        
        # windows
        else:
            return arquivo.split("\\")[-1]
    
    # retorna o diretorio dependendo do OS
    def __get_diretorio(diretorio):
        # linux
        if "/" in diretorio:
            return diretorio + "/"
        
        # windows
        else:
            return diretorio + "\\"

    # Upload de imagem no servidor
    def upload_image(self, arquivo):
        # define o diretorio de trabalho onde sera feito o upload
        self.set_wd(self.__wd)

        try:
            try:
                # abre o arquivo
                with open(arquivo, "rb") as file:
                    arquivo_upload = Servidor.__get_arquivo(arquivo)

                    # upload
                    ret = self.__ftp.storbinary(f'STOR {arquivo_upload}', file, blocksize = 1024*1024)
                    
                    # fecha o arquivo
                    file.close()
                
                # mensagem de retorno: 226 = sucesso
                return ret.startswith("226")
            
            except FileNotFoundError:
                print(f"\"{arquivo}\" nao encontrado")
                return False
        
        except ftplib.error_perm as e:
            print(f"Erro: {e}")
            return False
    
    # Download de imagem no servidor
    def download_image(self, arquivo, diretorio_destino):
        # define o diretorio de trabalho onde sera feito o download
        self.set_wd(self.__wd)

        try:
            # verifica se o diretorio de destino existe na maquina do usuario
            if not os.path.exists(diretorio_destino):
                print("Diretorio inexistente.")
                return False

            # verifica se o arquivo se encontra no diretorio de trabalho atual
            if arquivo not in self.get_files():
                print(f"\"{arquivo}\" inexistente.")
                return False
            
            destino = Servidor.__get_diretorio(diretorio_destino)

            # abre o arquivo
            with open(f"{destino}{arquivo}", "wb") as file:
                # download
                ret = self.__ftp.retrbinary(f"RETR {arquivo}", file.write)

                # fecha o arquivo
                file.close()
            
            # mensagem de retorno: 226 = sucesso
            return ret.startswith("226")
            
        except ftplib.error_perm as e:
            print(f"Erro: {e}")
            return False
    
    # Deletar uma imagem do servidor
    def delete_image(self, arquivo):
        # define o diretorio de trabalho onde se deletara um arquivo 
        self.set_wd(self.__wd)
 
        try:
            # verifica se o arquivo se encontra no diretorio de trabalho atual
            if arquivo not in self.get_files():
                print(f"\"{arquivo}\" nao encontrado.")
                return False
            
            # deleta o arquivo
            ret = self.__ftp.delete(arquivo)

            # mensagem de retorno: 250 = sucesso
            return ret.startswith("250")

        except ftplib.error_perm as e:
            print(f"Erro {e}")
            return False
        
    # Renomear uma imagem no servidor
    def rename_image(self, arquivo, novo_nome):
        # define o diretorio de trabalho onde se alterara o nome de uma imagem
        self.set_wd(self.__wd)

        try:
            # verifica se o arquivo se encontra no diretorio de trabalho atual
            if arquivo not in self.__ftp.nlst():
                print(f"\"{arquivo}\" nao encontrado.")
                return False

            # preserva a identificacao do tipo da imagem no novo nome
            novo_nome += '.' + arquivo.split('.')[-1]

            # renomeia o arquivo
            ret = self.__ftp.rename(arquivo, novo_nome)

            # mensagem de retorno: 250 = sucesso
            return ret.startswith("250")
        
        except ftplib.error_perm as e:
            print(f"Erro: {e}")
            return False
