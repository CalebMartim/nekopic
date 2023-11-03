import ftplib
import os

class Servidor:
    def __init__(self,host,user,password,wd = None):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__wd = None
        self.__ftp = ftplib.FTP_TLS()

    def get_ftp(self):
        return self.__ftp

    def connect(self):
        self.__ftp.connect(host=self.__host)

    def login(self):
        self.__ftp.login(user=self.__user,passwd=self.__password)

    def secure_data_connection(self):
        self.__ftp.prot_p()

    def quit(self):
        self.__ftp.quit()

    def set_wd(self, new_wd):
        try:
            if new_wd == self.__wd: return

            self.__wd = new_wd
            self.__ftp.cwd(self.__wd)

        except ftplib.error_perm as e:
            print(f"Erro: {e}")
            return

    def upload_image(self, arquivo):
        try:
            with open(arquivo, "rb") as file:
                ret = self.__ftp.storbinary(f'STOR {arquivo.split("/")[-1]}', file, blocksize = 1024*1024)
                file.close()
            
            return ret.startswith("226")
        
        except IOError:
            print("Arquivo não encontrado. Verifique o caminho.")
            return False
        
    def download_image(self, diretorio_origem, arquivo, diretorio_destino):
        try:
            if diretorio_origem != None:
                self.set_wd(diretorio_origem)

            if not os.path.exists(diretorio_destino):
                print("Diretorio inexistente.")
                return False

            if arquivo in self.__ftp.nlst():
                with open(f"{diretorio_destino}/{arquivo}", "wb") as file:
                    ret = self.__ftp.retrbinary(f"RETR {arquivo}", file.write)
                    file.close()
                
                return ret.startswith("226")
            else:
                print("Arquivo inexistente.")
                return False
        except ftplib.error_perm as e:
            print(f"Erro: {e}")
            return False