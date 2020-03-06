import socket
import select
import sys

# Configuracao do socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Checa se a quantidade de parametros esta correta
if len(sys.argv) != 3:
	print("Numero de parametros incorreto. Utilize servidor ip porta")
	exit()

# enderecoIP = primeiro argumento
enderecoIP = str(sys.argv[1])

# porta = segundo argumento
porta = int(sys.argv[2])

servidor.connect((enderecoIP, porta))

while True:
	# Mantem uma lista de possiveis input streams
	listaDeSockets = [sys.stdin, servidor]

	# O cliente tem duas situacoes: 
	# 1. Enviar uma mensagem para o servidor
	# 2. Exibir uma mensagem que o servidor enviou
	# Ao receber e exibir uma mensagem do servidor -> if = true
	# Ao enviar uma mensagem para o servidor -> else = true
	socketsDeLeitura, socketDeEscrita, socketDeErro = select.select(listaDeSockets,[],[])

	for sockets in socketsDeLeitura:
		if sockets == servidor:
			mensagem = sockets.recv(2048)
			print(mensagem.decode())
		else:
			mensagem = sys.stdin.readline()
			servidor.send(mensagem.encode())
			sys.stdout.write("[Voce]: ")
			sys.stdout.write(mensagem)
			sys.stdout.flush()
servidor.close()