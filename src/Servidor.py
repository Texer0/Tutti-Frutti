import socket
import threading
import asyncio
import Tuti

HOST = ''
PORT = 65125
HEADER = 10
CLIENTES = []
results = []

import os
try:
    if os.path.exists('temas.txt'):
        os.remove('temas.txt')
except FileNotFoundError:
    pass
except Exception as e:
    print(e)

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(3)
        print(f"Servidor escuchando en {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=run_async_in_thread, args=(handle_client, conn, addr))
            thread.start()

def run_async_in_thread(async_func, *args):
    asyncio.run(async_func(*args))
    


def send_text(conn, body):
    try:
        body = str(body)
        body = body.encode('utf-8')
        header = f"{len(body):<{HEADER}}"
        message = header.encode('utf-8') + body
        conn.send(message)
    except Exception as e:
        print(f"[DEVELOPMENT] Error al enviar el mensaje: {e}")

async def recive_data(conn):
    header_input = await asyncio.get_event_loop().sock_recv(conn, HEADER)
    if header_input:
        try:
            int(header_input.decode('utf-8'))
        except Exception as e:
            print(e)
        header_input = int(header_input.strip())
        data = await asyncio.get_event_loop().sock_recv(conn, header_input)
        data = data.decode('utf-8')
        if data == 'quit':
            raise Exception(f"Se ha cerrado la conexión desde el cliente")
        print(data)
        return data
    

async def handle_client(conn, addr):
    print(f'Conectado a la dirección: {addr}')
    send_text(conn, '\nBIENVENIDO/A A TUTTI FRUTTI\n')
    send_text(conn, 'Ingrese un nombre de usuario')
    name = await recive_data(conn)
    CLIENTES.append({'User':(name, addr, conn), 'answers':[]})
    try:         
        result = await Tuti.game(conn, {'User':(name, addr, conn), 'answers':[]})
        results.append(result)
        while True:
            if len(CLIENTES) == len(results):
                print(results)
                for resultado in results:
                    send_text(conn, f'\nResultados: {resultado}')
                    print(resultado)
                break
        send_text(conn, '¿Desea jugar de nuevo? Si/No')
        input_user = await recive_data(conn)
        if input_user.lower() == 'si':
            iniciar_servidor()
        elif input_user.lower() == 'no':
            raise Exception(f"Se ha cerrado la conexión desde el cliente")
    except Exception as e:
        print('Ocurrió un error al ejecutar el juego:', e)
    finally:
        conn.close()



if __name__ == "__main__":
    try:
        iniciar_servidor()
    except Exception as e:
        print(f"[DEVELOPMENT] Error al iniciar el servidor: {e}")
