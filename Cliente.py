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

    def download(self, arquivos: list[str], destino: str):
        falhas: list[str] = []

        for arquivo in arquivos:
            if self.servidor.download_image(arquivo, destino):
                continue
            else:
                falhas.append(arquivo)

        if falhas:
            return falhas
        else:
            return True

    def delete(self, arquivos: set):
        falhas: list[str] = []

        for arquivo in arquivos:
            if self.servidor.delete_image(arquivo):
                continue
            else:
                falhas.append(arquivo)
        if falhas:
            return falhas
        else:
            return True

    def renomear(self, old: str, new: str) -> bool:
        return self.servidor.rename_image(old, new)
