import socket 
import select 
import sys 
from thread import *

# Configuracoes do socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Checa se a quantidade de parametros esta correta
if len(sys.argv) != 3:
	print "Numero de parametros incorreto. Utilize servidor ip porta"
	exit()

# enderecoIP = primeiro argumento
enderecoIP = str(sys.argv[1])

# porta = segundo argumento
porta = int(sys.argv[2])

# Liga o servidor a tupla (enderecoIP, porta)
servidor.bind((enderecoIP, porta))

# Habilia o servidor a aceitar conexoes, 10 -> numero maximo de conexoes
servidor.listen(10)

print("Servidor iniciado.\nIP: " + enderecoIP + "\n" +"Porta: " + str(porta))

# Lista de clientes, inicialmente vazia
listaDeClientes = []

def threadDoCliente(conexao, endereco):

	# Envia uma mensagem ao cliente cujo objeto e conexao
	conexao.send("Entrou no chat.")

	while True:
		try:
			# Recebe dados do do socket, 2048 -> buffer size
			mensagem = conexao.recv(2048) 

			# Ao receber a mensagem
			if mensagem: 

				# Mostra quem mandou a mensagem + a mensagem
				print "[" + endereco[0] + "]: " + mensagem 

				# Chama a funcao transmitir para enviar a mensagem para todos os clientes
				mensagemTransmitida = "[" + endereco[0] + "]: " + mensagem 
				transmitir(mensagemTransmitida, conexao) 

			else: 
				# Se a mensagem nao houver conteudo, remove a conexao
				remove(conn)

		except: 
			continue

# Transmite a mensagem para todos os clientes com objeto diferente do cliente que enviou
def transmitir(mensagem, conexao):
	for clientes in listaDeClientes:
		if clientes!=conexao:
			try:
				clientes.send(mensagem)
			except:
				clientes.close()

				# Se a conexao estiver quebrada, remove-a
				remove(clients)

# Remove o cliente da listaDeClientes
def remover(conexao): 
	if conexao in listaDeClientes: 
		listaDeClientes.remove(conexao)

while True: 

	# Aceita a conexao e guarda dois parametros
	# conexao -> objeto socket do cliente
	# endereco -> endereco IP do cliente
	conexao, endereco = servidor.accept() 

	# Insere a conexao na lista de clientes
	listaDeClientes.append(conexao) 

	# Mostra o endereco do cliente que se conectou
	print endereco[0] + " se conectou"

	# Cria uma thread individual para cada cliente
	start_new_thread(threadDoCliente,(conexao,endereco))	 

conexao.close() 
servidor.close()  