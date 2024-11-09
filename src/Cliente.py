import socket
from time import sleep
import asyncio
import threading

HOST = ''
PORT = 65125
HEADER = 10

def send_text(conn, body):
    sleep(0.1)
    try:
        lenght = len(body) + HEADER
        header = f"{lenght:<{HEADER}}"
        message = header + body
        conn.send(message.encode('utf-8'))
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")
        
        
async def recive_data(conn):
    while True:
        try:
            header_input = await asyncio.get_event_loop().sock_recv(conn, HEADER)
            if header_input:
                header_input = int(header_input.strip())
                if isinstance(header_input, int):
                    data = await asyncio.get_event_loop().sock_recv(conn, header_input)
                    print(data.decode('utf-8'))
        except Exception as e:
            print(e)
            break


def iniciar():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        hilo_recepcion = threading.Thread(target=run_async_in_thread, args=(recive_data, s))
        hilo_recepcion.start()

        while True:
            input_message = input("")
            if input_message == 'quit':
                send_text(s, input_message)
                print("Se ha cerrado la conexión")
                break
            send_text(s, input_message)

def run_async_in_thread(async_func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(async_func(*args))
    except asyncio.CancelledError:
        pass
    finally:
        loop.close()
        
if __name__ == "__main__":
    try:
        iniciar()
    except Exception as e:
        print("[DEVELOPMENT] Se cerró el socket")