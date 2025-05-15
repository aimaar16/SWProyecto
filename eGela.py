# -*- coding: UTF-8 -*-
from tkinter import messagebox
import requests
import urllib
from urllib.parse import unquote
from bs4 import BeautifulSoup
import time
import helper

class eGela:
    _login = 0
    _cookie = ""
    _curso = ""
    _refs = []
    _root = None

    def __init__(self, root):
        self._root = root

    def check_credentials(self, username, password, event=None):
        popup, progress_var, progress_bar = helper.progress("check_credentials", "Logging into eGela...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("##### 1. PETICION #####")
        metodo = 'GET'
        uri = "https://egela.ehu.eus/login/index.php"
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################
        cabeceras = {'Host': 'egela.ehu.eus'}
        print("SOLICITUD 1\n" + metodo + " " + uri + " HTTP/1.1")
        respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
        cookie = respuesta.headers.get('Set-Cookie')
        cookieFinal = cookie.split(';')[0]
        codigo = respuesta.status_code
        print("Cookie extraida: " + cookieFinal)

        html = BeautifulSoup(respuesta.text, 'html.parser')
        logintoken = html.find('input', attrs={'name': 'logintoken'})['value']
        print("Logintoken: " + logintoken)
        print("Codigo: " + str(codigo) + "\n")

        progress = 25
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)


        print("\n##### 2. PETICION #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

        metodo2 = 'POST'
        cabeceras2 = {'Host': 'egela.ehu.eus', 'Content-type': 'application/x-www-form-urlencoded',
                      'Cookie': cookieFinal}
        cuerpo = {'logintoken': logintoken, 'username': username.get(),
                  'password': password.get()}
        cuerpo_encoded = urllib.parse.urlencode(cuerpo)

        respuesta2 = requests.request(metodo2, uri, data=cuerpo_encoded, headers=cabeceras2, allow_redirects=False)
        codigo = respuesta2.status_code
        print("SOLICITUD 2\n" + metodo2 + " " + uri + " HTTP/1.1")
        print("Cookie extraida: " + cookieFinal)
        print("Logintoken: " + logintoken)
        print("Codigo: " + str(codigo) + "\n")



        progress = 50
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)

        print("\n##### 3. PETICION #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

        uri = respuesta2.headers['Location']
        cookie = respuesta2.headers.get('Set-Cookie')
        cookieFinal = cookie.split(';')[0]

        metodo3 = 'GET'
        cabeceras3 = {'Host': 'egela.ehu.eus', 'Cookie': cookieFinal}

        respuesta3 = requests.request(metodo3, uri, data=cuerpo_encoded, headers=cabeceras3, allow_redirects=False)
        codigo = respuesta3.status_code
        print("SOLICITUD 3\n" + metodo3 + " " + uri + " HTTP/1.1")
        print("Cookie extraida: " + cookieFinal)
        print("Logintoken: " + logintoken)
        print("Codigo: " + str(codigo) + "\n")

        progress = 75
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)
        popup.destroy()

        print("\n##### 4. PETICION #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

        uri = respuesta3.headers['Location']
        metodo4 = 'GET'
        cabeceras4 = {'Host': 'egela.ehu.eus', 'Cookie': cookieFinal}

        respuesta4 = requests.request(metodo4, uri, data=cuerpo_encoded, headers=cabeceras4, allow_redirects=False)
        codigo = respuesta4.status_code
        print("SOLICITUD 4\n" + metodo4 + " " + uri + " HTTP/1.1")
        print("Cookie extraida: " + cookieFinal)
        print("Logintoken: " + logintoken)
        print("Codigo: " + str(codigo) + "\n")

        progress = 100
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)
        popup.destroy()

        html = BeautifulSoup(respuesta4.text, 'html.parser')
        for div in html.find_all('div', {'class': 'w-100'}):
            for a in div.find_all('a'):
                if 'Sistemas Web' in a.get_text():
                    enlace = a.get('href')
                    break

        if codigo==200:
            #############################################
            # ACTUALIZAR VARIABLES
            #############################################
            self._login = 1
            self._cookie=cookieFinal
            self._curso=enlace
            self._root.destroy()
        else:
            messagebox.showinfo("Alert Message", "Login incorrect!")

    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 4. PETICION (Página principal de la asignatura en eGela) #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

        uri = self._curso
        metodo4 = 'GET'
        cabeceras4 = {'Host': 'egela.ehu.eus', 'Cookie': self._cookie}

        respuesta4 = requests.request(metodo4, uri, headers=cabeceras4, allow_redirects=False)
        codigo = respuesta4.status_code
        print(codigo)

        enlaceCabeceras = {}
        html = BeautifulSoup(respuesta4.text, 'html.parser')
        for div in html.find_all('div', {'class': 'tabs-wrapper'}):
            for li in div.find_all('li'):
                a = li.find('a')
                nombre = a.text.replace('Destacado', '').strip()
                enlaceCabeceras[nombre] = a.get('href')
                print(f"{nombre}: {enlaceCabeceras[nombre]}")


        progress_step = float(100.0 / len(enlaceCabeceras))


        print("\n##### Analisis del HTML... #####")
        #############################################
        # ANALISIS DE LA PAGINA DEL AULA EN EGELA
        # PARA BUSCAR PDFs
        #############################################
        for nombre, enlace in enlaceCabeceras.items():
            # Acceder a la página de la sección
            respuesta = requests.request(metodo4, enlace, headers=cabeceras4,allow_redirects=False)

            if respuesta.status_code != 200:
                print(f"Error al acceder a {enlace}: Código {respuesta.status_code}")
                continue
            html = BeautifulSoup(respuesta.text, 'html.parser')
            recursosLink = []
            for div in html.find_all('div', {'class': 'activityname'}):
                for a in div.find_all('a'):
                    link = a.get('href')
                    if link and "/mod/resource/view.php" in a.get('href'):
                        link = a.get('href')
                        self._refs.append({'pdf_name': a.get_text(strip=True), 'pdf_link': link})
                        progress_step = float(100.0 / len(self._refs))
                        progress += progress_step
                        progress_var.set(progress)
                        progress_bar.update()
                        time.sleep(0.1)

        # INICIALIZA Y ACTUALIZAR BARRA DE PROGRESO
        # POR CADA PDF ANIADIDO EN self._refs



        popup.destroy()
        return self._refs

    def get_pdf(self, selection):

        print("\t##### descargando  PDF... #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################
        cabecera = {
            'Cookie': self._cookie
        }
        pdf=self._refs[selection]
        pdf_name=pdf['pdf_name']+".pdf"
        pdf_link=pdf['pdf_link']
        pdf_response = requests.request('GET', pdf_link, headers=cabecera, allow_redirects=False)
        pdf_content = requests.request('GET', pdf_response.headers['Location'], headers=cabecera, allow_redirects=False)
        return pdf_name, pdf_content