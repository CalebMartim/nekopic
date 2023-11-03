from Servidor import Servidor

def introducao():
    ret = f"Digite:\n\t1.Upload\n\t2.Download\n"
    return ret

servidor = Servidor("192.168.37.73","servidor_redes","servidorredes123")
servidor.connect()
servidor.login()
servidor.secure_data_connection()
servidor.set_wd("/files/images")

if servidor.get_ftp().getwelcome().startswith("220"): 
    print("Bem-vindo!")

    while True:
        try:
            comando = int(input(introducao()))

            if comando == 1:
                arquivo = input("Digite o caminho do arquivo: ")

                if servidor.upload_image(arquivo):
                    print("Upload com sucesso")
                else:
                    print("Upload fracassado")

            elif comando == 2:
                origem = input("Digite o diretorio onde o arquivo se localiza: ")
                if origem == "": origem = None

                arquivo = input("Digite o nome do arquivo: ")
                destino = input("Digite o caminho de destino do arquivo: ")

                if servidor.download_image(origem, arquivo, destino):
                    print("Download com sucesso")
                else:
                    print("Download fracassado")

            else: break

            print()
        
        except ValueError:
            print("Comando inválido")

    # Sai do servidor
    servidor.quit()

print("acabou...")
