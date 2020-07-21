import socket

# Configuracao do socket
socket_servidor = socket.socket()

# Entrada de endereco IP
entrada_endereco = str(input("Endereco (use lcl para transferencia local): "))

# Entrada de porta
porta = int(input("Porta: "))

# Se a entrada for "lcl" -> endereco = hostname
if(entrada_endereco == "lcl"):
    endereco = socket.gethostname()
else:
    endereco = entrada_endereco

# Liga o socket a tupla endereco porta
socket_servidor.bind((endereco, porta))

# Pode receber ate 5 conexoes
socket_servidor.listen(5)

# Arquivo a ser recebido, write binary
arquivo_para_receber = open("para_receber.txt", "wb")

# Loop do servidor
while True:
    # Conexao com cliente
    socket_cliente, endereco_cliente = socket_servidor.accept()
    print("Conexao com o cliente " + str(endereco))

    # Loop para receber pacotes do cliente
    pacote = socket_cliente.recv(1024)
    print("Pacote recebido")
    while(pacote):
        arquivo_para_receber.write(pacote)
        pacote = socket_cliente.recv(1024)
        print("Pacote recebido")

    # Fecha o arquivo recebido e encerra a conexao
    arquivo_para_receber.close()
    socket_cliente.close()
    print("Fim da conexao com o cliente " + str(endereco))
