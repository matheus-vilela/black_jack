import socket, os
import time

def client(host = 'localhost', port=8082): 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_address = (host, port) 
    os.system('cls' if os.name == 'nt' else 'clear')
    print ("Connecting to %s port %s" % server_address) 
    sock.connect(server_address) 
    try: 
        nome = "banca" 
        print ("Enviando nome %s" % nome) 
        sock.sendall(nome.encode('utf-8')) 
        amount_received = 0 
        amount_expected = len(nome) 
        while amount_received < amount_expected: 
            data = sock.recv(16) 
            amount_received += len(data) 
            print ("Recebido: %s" % data)
            while True:
                time.sleep(1.5)

    except socket.error as e: 
        print ("Socket error: %s" %str(e))

    except Exception as e: 
        print ("Other exception: %s" %str(e)) 

    finally: 
        print ("Finalizando conexão no servidor...") 
        sock.close() 

client()