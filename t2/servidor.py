import socket
import time

# Tamanho do pacote
tamanho_pacote = 1024

# Configuracao do socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
socket_servidor.listen(1)

# Arquivo a ser recebido, write binary
arquivo_para_receber = open("para_receber.rar", "wb")

# Contador de pacotes
numero_pacotes = 0

# Loop do servidor
while True:
	# Conexao com cliente
	socket_cliente, endereco_cliente = socket_servidor.accept()
	print("Conexao com o cliente " + str(endereco_cliente[0]))

	# Tempo no inicio da conexao
	tempo_conexao_1 = time.perf_counter() 

	# Loop para receber pacotes do cliente
	pacote = socket_cliente.recv(tamanho_pacote)
	numero_pacotes += 1
	
	while(pacote):
		arquivo_para_receber.write(pacote)
		pacote = socket_cliente.recv(tamanho_pacote)
		numero_pacotes += 1

	# Tempo no fim da conexao
	tempo_conexao_2 = time.perf_counter() 

	# Fecha o arquivo recebido e encerra a conexao
	arquivo_para_receber.close()
	socket_cliente.close()

	tempo_total = tempo_conexao_2 - tempo_conexao_1
	tamanho_total = numero_pacotes * tamanho_pacote

	print("Fim da conexao com o cliente " + str(endereco_cliente[0]))
	print("Tempo de conexao: " + str(tempo_total) "segundos")
	print("Numero de pacotes: " + str(numero_pacotes))
	print("Tamanho do arquivo: " + str(tamanho_total) + "bits")
	print("Velocidade de transferencia: " + str(tamanho_total/tempo_total) + "bits/segundo")