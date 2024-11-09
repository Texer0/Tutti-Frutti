import Servidor
import random
import os

letra = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
async def game(conn, cliente):

    async def tuti_fruti(temas, letra):
        Servidor.send_text(conn, f'La letra elegida es: {letra.upper()}')
        print(cliente)
        print(cliente['answers'])
        print(cliente['User'][0]) # NAME
        result = ''
        for tema in temas:
            Servidor.send_text(conn, f"\nLetra: {letra.upper()} \nTema: {tema}")
            answer = await Servidor.recive_data(conn)
            # if not cliente['answers']:
            cliente['answers'].append({tema:answer})
            result = f'\nUsuario: {cliente['User'][0].capitalize()}\nRespuestas: {cliente['answers']}\n'
        return result

    while True:
        
        Servidor.send_text(conn, "\nAñada un tema al juego: \n Texto -> Añadir un tema \n 'jugar' -> Iniciar juego \n 'resultados' -> Ver las respuestas \n")
        input_usuario = await Servidor.recive_data(conn)
        
        def contiene_numeros(texto):
            try:
                numeros = list(map(str, range(1, 11)))
                for numero in numeros:
                    if numero in texto:
                        return True
                return False
            except Exception as e:
                pass
        if input_usuario == "resultados":
            print("Esperando al resto de jugadores...")
            Servidor.send_text(conn, "\nEsperando al resto de jugadores...")
            return result
        elif input_usuario == "jugar":
            try:
                    with open('temas.txt', 'r') as file:
                        temas = file.read().splitlines()
                        if temas:                  
                            print(f'\n{temas}')
                            Servidor.send_text(conn, temas)
                            result = await tuti_fruti(temas, letra)
            except Exception as e:
                pass
            try:
                with open('temas.txt', 'w') as file:
                    pass
                if not result:
                    Servidor.send_text(conn, "\nPor favor coloque un tema")
                continue
            except Exception as e:
                print(e)

        elif contiene_numeros(input_usuario) or input_usuario == '':
            Servidor.send_text(conn, "Por favor coloque un tema")
        else:
            with open('temas.txt', 'a+') as file:
                if not input_usuario in file.read():
                    file.write(f'{input_usuario}\n')
                    Servidor.send_text(conn, '\nOpción añadida')
                else:
                    Servidor.send_text(conn, "El tema ya fué seleccionado")
            