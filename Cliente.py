# importa a classe Servidor
from Servidor import Servidor


class Cliente:
    def __init__(self):
        # entrar no servidor
        self.servidor = Servidor("192.168.68.122", "servidor_redes", "servidorredes123")
        self.servidor.connect()
        self.servidor.login()
        self.servidor.set_wd("/files/images")

        # conexao TLS
        self.servidor.secure_data_connection()

        self.conectar()

        # servidor.quit()

    def conectar(self) -> bool:
        return self.servidor.get_ftp().getwelcome().startswith("220")

    def upload(self, arquivo: str) -> bool:
        return self.servidor.upload_image(arquivo)

    def download(self, arquivos, destino: str):
        falhas = []

        for arquivo in arquivos:
            if self.servidor.download_image(arquivo, destino):
                continue
            else:
                falhas.append(arquivo)

        if falhas:
            return False, falhas
        else:
            return True, falhas

    def delete(self, arquivos: dict):
        falhas = []

        for arquivo in arquivos.keys():
            if self.servidor.delete_image(arquivo):
                continue
            else:
                falhas.append(arquivo)
        if falhas:
            return False, falhas
        else:
            return True, falhas

    def renomear(self, old: str, new: str) -> bool:
        return self.servidor.rename_image(old, new)

    def imagens(self):
        return self.servidor.imagens()
