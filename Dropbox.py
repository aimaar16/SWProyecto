import requests
import urllib
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json
import helper

app_key = '7qq7k4bsxss0wmo'
app_secret = 'ay3qf2s6vqzf11a'
server_addr = "localhost"
server_port = 8090
redirect_uri = "http://" + server_addr + ":" + str(server_port)

class Dropbox:
    _access_token = ""
    _path = ""
    _files = []
    _root = None
    _msg_listbox = None

    def __init__(self, root):
        self._root = root

    def local_server(self):
        # por el puerto 8090 esta escuchando el servidor que generamos
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((server_addr, server_port))
        server_socket.listen(1)
        print("\tLocal server listening on port " + str(server_port))

        # recibe la redireccio 302 del navegador
        client_connection, client_address = server_socket.accept()
        peticion = client_connection.recv(1024)
        print("\tRequest from the browser received at local server:")
        print (peticion)

        # buscar en solicitud el "auth_code"
        primera_linea =peticion.decode('UTF8').split('\n')[0]
        aux_auth_code = primera_linea.split(' ')[1]
        auth_code = aux_auth_code[7:].split('&')[0]
        print ("\tauth_code: " + auth_code)

        # devolver una respuesta al usuario
        http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                        "<html>" \
                        "<head><title>Proba</title></head>" \
                        "<body>The authentication flow has completed. Close this window.</body>" \
                        "</html>"
        client_connection.sendall(http_response)
        client_connection.close()
        server_socket.close()

        return auth_code

    def do_oauth(self):
        #############################################
        # RELLENAR CON CODIGO DE LAS PETICIONES HTTP
        # Y PROCESAMIENTO DE LAS RESPUESTAS HTTP
        # PARA LA OBTENCION DEL ACCESS TOKEN
        #############################################
        params = {
            'client_id': app_key,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'token_access_type': 'offline'
        }
        url = f"https://www.dropbox.com/oauth2/authorize?{urllib.parse.urlencode(params)}"
        print(f"\tAbriendo navegador para autorizar...\n\t{url}")
        webbrowser.open_new(url)
        auth_code = self.local_server()

        print("Step 3.- Intercambiando el código por un token de acceso...")

        uri = "https://api.dropboxapi.com/oauth2/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'code': auth_code,
            'client_id': app_key,
            'client_secret': app_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

        response = requests.post(uri, headers=headers, data=data)
        if response.status_code != 200:
            print("Error al obtener el token:", response.text)
            return None

        token_json = response.json()
        access_token = token_json['access_token']
        print(f"\tAccess Token: {access_token}")
        self._access_token = access_token

        self._root.destroy()

    def list_folder(self, msg_listbox):
        print("/list_folder")
        uri = 'https://api.dropboxapi.com/2/files/list_folder'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-list_folder
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################
        uri = 'https://api.dropboxapi.com/2/files/list_folder'
        headers = {
            'Authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json'
        }
        data = {
            "path": self._path,
            "include_deleted": False,
            "include_has_explicit_shared_members": False,
            "include_media_info": False,
            "include_mounted_folders": True,
            "include_non_downloadable_files": True,
            "recursive": False
        }

        respuesta = requests.post(uri, headers=headers, json=data)
        contenido_json = respuesta.json()
        for carpeta in contenido_json.get('entries'):
            print(f"- {carpeta['name']}")
            uri = 'https://content.dropboxapi.com/2/files/download'
            print(carpeta['path_display'])
            headers = {
                'Authorization': 'Bearer ' + self._access_token,
                'Dropbox-API-Key': {'path': carpeta['path_display']}
            }
            respuesta = requests.post(uri, headers=headers)
            if respuesta.status_code != 200:
                print("Error al obtener carpetas:", respuesta.text)
                return
        self._files = helper.update_listbox2(msg_listbox, self._path, contenido_json)

    def transfer_file(self, file_path, file_data):
        print("/upload")
        uri = 'https://content.dropboxapi.com/2/files/upload'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-upload
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

    def delete_file(self, file_path):
        print("/delete_file")
        uri = 'https://api.dropboxapi.com/2/files/delete_v2'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-delete
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

    def create_folder(self, path):
        print("/create_folder")
       # https://www.dropbox.com/developers/documentation/http/documentation#files-create_folder
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################
