import socket

# Configuracao do socket
socket_cliente = socket.socket()

# Entrada de endereco IP
entrada_endereco = str(input("Endereco (use lcl para transferencia local): "))

# Entrada de porta
porta = int(input("Porta: "))

# Se a entrada for "lcl" -> endereco = hostname
if(entrada_endereco == "lcl"):
    endereco = socket.gethostname()
else:
    endereco = entrada_endereco

# Se conecta com a tupla endereco porta
socket_cliente.connect((endereco, porta))
print("Conexao com o servidor " + str(endereco));

# Arquivo a ser enviado
arquivo_para_enviar = open("para_enviar.txt", "rb")

# Le 1024b do arquivo a ser enviado
pacote = arquivo_para_enviar.read(1024)

# Loop de leitura e envio
while(pacote):
    socket_cliente.send(pacote)
    print("Pacote enviado")
    pacote = arquivo_para_enviar.read(1024)

# Fecha o arquivo e encerra a conexao
arquivo_para_enviar.close()
socket_cliente.shutdown(socket.SHUT_WR)
print("Fim da conexao com o servidor " + str(endereco))