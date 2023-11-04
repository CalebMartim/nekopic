# importa a classe Servidor
from Servidor import Servidor

# funcao de introducao do programa: apresenta as operacoes do servidor


def introducao():
    ret = f"Digite:\n\t1.Upload\n\t2.Download\n\t3.Deletar\n\t4.Renomear arquivo\n\t0.Sair\n"
    return ret


# entrar no servidor
servidor = Servidor("192.168.68.122", "servidor_redes", "servidorredes123")
servidor.connect()
servidor.login()
servidor.set_wd("/files/images")

# conexao TLS
servidor.secure_data_connection()

# se conseguimos conectar ao servidor, uma mensagem de bem-vindo é gerada
if servidor.get_ftp().getwelcome().startswith("220"): 
    print("Bem-vindo!")

    # loop principal do programa
    while True:
        try:
            comando = int(input(introducao()))

            # Upload de imagens
            if comando == 1:
                # path de onde se encotra(m) o(s) arquivo(s) para ser(em) enviado(s) ao servidor
                arquivos = input("Digite o caminho do(s) arquivo(s): ").split()

                # para cada arquino na lista de arquivos para upload
                for arquivo in arquivos:
                    if servidor.upload_image(arquivo):
                        print("Upload com sucesso")

                    else:
                        print("Upload fracassado")

            # Download de imagens
            elif comando == 2:
                # nome do(s) arquivo(s) no servidor
                arquivos = input("Digite o(s) nome(s) do(s) arquivo(s): ").split()

                # onde sera armazenado o(s) arquivo(s) desejado(s)
                destino = input("Digite o caminho de destino do(s) arquivo(s): ")

                # para cada arquivo na lista de arquivos para download
                for arquivo in arquivos:
                    if servidor.download_image(arquivo, destino):
                        print("Download com sucesso")
                    
                    else:
                        print("Download fracassado")

            # Deletar arquivos do servidor
            elif comando == 3:
                # nome do arquivo a ser deletado do servidor
                arquivo = input("Digite o nome do arquivo a ser deletado do servidor: ")
                
                if servidor.delete_image(arquivo):
                    print("Arquivo deletado com sucesso")
                
                else:
                    print("Nao foi possivel deletar o arquivo")
            
            # Renomear um arquivo do servidor
            elif comando == 4:
                # nome do arquivo no servidor a ser renomeado
                arquivo = input("Digite o nome do arquivo que voce deseja renomear: ")

                # novo nome do arquivo desejado
                novo_nome = input("Digite o novo nome: ")

                if servidor.rename_image(arquivo, novo_nome):
                    print("Nome alterado com sucesso")

                else:
                    print("Nao foi possivel alterar o nome do arquivo")

            # sair do loop 
            elif comando == 0: 
                break

            # quebra de linha da proxima exibicao da mensagem de introducao
            print()
        
        # caso seja fornecido outro tipo de entrada
        except ValueError:
            print("Comando inválido\n")

    # Sair do servidor
    servidor.quit()


# caso contrario
else:
    print("Nao foi possivel entrar no servidor.")
