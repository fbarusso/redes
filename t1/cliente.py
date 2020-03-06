import socket
import select
import sys

# Configuracoes do socket.
socketDoServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketDoServidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Checa se os parametros estao corretos.
if len(sys.argv) != 3:
	print("Parametros incorretos. Utilize cliente enderecoDoServidor portaDoServidor")
	exit()

nickname = str(input("Nickname: "))

# Primeiro agumento -> enderecoDoServidor. Segundo argumento -> portaDoServidor.
enderecoDoServidor = str(sys.argv[1])
portaDoServidor = int(sys.argv[2])

# Conecta ao servidor.
socketDoServidor.connect((enderecoDoServidor, portaDoServidor))


# Loop do cliente.


while True:
	# Mantem uma lista de possiveis input streams (input do sistema e servidor).
	listaDeInputStreams = [sys.stdin, socketDoServidor]

	# O cliente tem duas situacoes: 
	# 1. Enviar uma mensagem para o servidor.
	# 2. Exibir uma mensagem que o servidor enviou.
	# O select espera ate que um dos file descriptors esteja pronto para operacoes I/O.
	# Ao receber e exibir uma mensagem do servidor -> if = true.
	# Ao enviar uma mensagem para o servidor -> else = true.
	socketsDeLeitura, socketDeEscrita, socketDeErro = select.select(listaDeInputStreams,[],[])

	for sockets in socketsDeLeitura:
		# Receber mensagem do servidor.
		if sockets == socketDoServidor:
			mensagem = sockets.recv(2048)
			print(mensagem.decode())

		# Enviar mensagem para o servidor.
		else:
			mensagem = sys.stdin.readline()
			socketDoServidor.send((" <" + nickname + "> " + mensagem).encode())
			sys.stdout.write("[Voce]: ")
			sys.stdout.write(mensagem)
			sys.stdout.flush()

socketDoServidor.close()