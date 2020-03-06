import socket
import select
import sys
import _thread

# Configuracoes do socket.
socketDoServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketDoServidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Checa se os parametros estao corretos.
if len(sys.argv) != 3:
	print("Parametros incorretos. Utilize servidor enderecoDoServidor portaDoServidor")
	exit()

# Primeiro agumento -> enderecoDoServidor. Segundo argumento -> portaDoServidor.
enderecoDoServidor = str(sys.argv[1])
portaDoServidor = int(sys.argv[2])

# Liga o socket do servidor a tupla (enderecoDoServidor, portaDoServidor).
socketDoServidor.bind((enderecoDoServidor, portaDoServidor))

# Habilia o socket do servidor a aceitar conexoes. 10 -> numero maximo de conexoes.
socketDoServidor.listen(10)

print("Servidor iniciado.\nIP: " + enderecoDoServidor + "\n" +"Porta: " + str(portaDoServidor))

# Lista de (sockets de) clientes, inicialmente vazia.
listaDeClientes = []


# Funcoes do servidor


def threadDoCliente(socketDoCliente, enderecoDoCliente):
	# Envia a mensagem ao socket do cliente. 
	# O metodo send aceita apenas bytes, por isso e necessario o encode.
	socketDoCliente.send("Entrou no chat.".encode())

	while True:
		try:
			# Recebe dados do do socket do cliente. 2048 -> buffer size.
			mensagemRecebida = socketDoCliente.recv(2048) 

			# Ao receber a mensagem.
			if mensagemRecebida: 
				# Mostra o endereco do cliente + a mensagem.
				# A mensagem chega em bytes, por isso e necessario o decode.
				print("[" + enderecoDoCliente[0] + "]: " + mensagemRecebida.decode()) 

				# Chama a funcao transmitirMensagem para enviar a mensagem para todos os clientes.
				mensagemASerTransmitida = "[" + enderecoDoCliente[0] + "]: " + mensagemRecebida 
				transmitirMensagem(mensagemASerTransmitida, socketDoCliente) 

			else:
				# Se a mensagem nao houver conteudo, remove o socket do cliente.
				remove(socketDoCliente)

		except:
			continue

# Transmite a mensagem para todos os clientes com objetos socket diferente de quem enviou
def transmitirMensagem(mensagemASerTransmitida, socketDoCliente):
	for cliente in listaDeClientes:
		if cliente!=socketDoCliente:
			try:
				# Envia a mensagem
				cliente.send(mensagemASerTransmitida.encode())
			except:
				# Se a socketDoCliente estiver quebrada, remove-a
				cliente.close()
				remove(clients)

# Remove o cliente da listaDeClientes
def remover(socketDoCliente): 
	if socketDoCliente in listaDeClientes: 
		listaDeClientes.remove(socketDoCliente)


# Loop do servidor


while True: 
	# Aceita a conexao e recebe dois retornos: socket do cliente e endereco do cliente.
	socketDoCliente, enderecoDoCliente = socketDoServidor.accept() 

	# Insere o socket do cliente na lista de clientes
	listaDeClientes.append(socketDoCliente) 

	# Mostra o endereco do cliente que se conectou
	print(enderecoDoCliente[0] + " se conectou")

	# Cria uma thread individual para cada cliente
	_thread.start_new_thread(threadDoCliente,(socketDoCliente, enderecoDoCliente))	 

socketDoCliente.close() 
socketDoServidor.close()  