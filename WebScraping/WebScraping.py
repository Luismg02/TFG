import requests #Nos permite realizar solicitudes webs.
from bs4 import BeautifulSoup #Nos permite analizar el HTML obtenido.
import sqlite3 #Para almacenar en una base de datos.
import re #Realizar operaciones de coincidencia de expresiones regulares 

# Realizo la solicitud HTTP con los parámetros que nos interesan (he obtenido estos parámetros haciendo una previa 
# búsqueda desde el navegador web).
url = "https://bugzilla.kernel.org/buglist.cgi" #url bugs
url_raiz_adjuntos = "https://bugzilla.kernel.org/" #url raiz para la busqueda de adjuntos

#Parametros que le paso a la petición GET.
params = {
    'api_key': 'bADPlASyNq9PWKVvpfT1IriTdcvy5Vzhwql8VjQE',
    'bug_status': '__all__',
    'content': '"BUG: KASAN:"',
    'limit' : 0, #para que no se nos limite las busquedas a 200 solo
    'no_redirect': '1',
    #'order': 'Importance',
    'query_format': 'specific'
}

#Respuesta de la peticion
respuesta = requests.get(url, params=params)

# Verificar si la solicitud tuvo exito o no.
if respuesta.status_code == 200:

    # Parseo el contenido HTML.
    soup = BeautifulSoup(respuesta.text, 'html.parser')

    # Encuentro los elementos que contienen informacion de bugs (hemos analizado la etiqueta y clase correspondiente donde se encuentran esos bugs).
    elementos_bugs = soup.find_all('tr', class_='bz_bugitem')

    # Inicializo una conexión a la base de datos (hemos usado SQLite3).
    conn = sqlite3.connect('borrame.db')
    cursor = conn.cursor()

    # Creo una tabla para almacenar la información que queremos sobre el bug (tipo, cve, mensaje del commit del usuario, archivos adjuntos, hardware al que afecta 
    #y url de la página de bugzilla donde esta reportado ese bug.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bugs (
            tipo TEXT,
            cve TEXT PRIMARY KEY,
            commit_mensaje TEXT,
            adjuntos TEXT,
            hardware TEXT,
            url TEXT
        )
    ''')
    conn.commit()
    
    # Itero sobre cada uno de los bugs para acceder y almacenar la información de ellos en la base de datos.
    urlbug = "https://bugzilla.kernel.org/show_bug.cgi" #raiz de la url donde se encuentra mas informacion sobre los bugs.

    for bug in elementos_bugs:

        # Obtenemos el ID del bug correspondiente
        bug_id = bug.find('td', class_='first-child bz_id_column').a.text.strip()

        #Obtenemos el parte del link del respectivo bug
        bug_link = bug.find('td', class_='first-child bz_id_column').a['href']
        
        params2 = {
            'api_key': 'bADPlASyNq9PWKVvpfT1IriTdcvy5Vzhwql8VjQE',
            'id': bug_id}
            
        #Hacemos la solicitud para cada bug con los parametros opcionales
        respuesta_bug = requests.get(urlbug, params=params2)

        if respuesta_bug.status_code == 200:
            
            # Parseo el contenido de la respuesta del servidor para ese bug en concreto.
            soup_bug = BeautifulSoup(respuesta_bug.content, 'html.parser')
            '''
            # Obtener el texto que existe dentro de la etiqueta <pre> que contiene el commit del usuario.
            soup_bug_texto = soup_bug.find('pre', class_='bz_comment_text').get_text()
            
            # Utilizo una expresión regular para encontrar la palabra después de 'KASAN:'
            match = re.search(r'BUG: ([kK][aA][sS][aA][nN]): (\S+)', soup_bug_texto)
            
            # Verificar si se encontró la palabra y extraerla. Primero busco la palabra en el commit del usuario, después en 
            #el titulo de la pagina del bug y por ultimo en cada uno de los comentarios del bug.
            if match:
                resultado = match.group(2)                      
            else:
                soup_bug_titulo = soup_bug.find("title").get_text()
                match = re.search(r'BUG: ([kK][aA][sS][aA][nN]): (\S+)', soup_bug_titulo)
                
                if match:
                    resultado = match.group(2)
                    
                else:
                    soup_bug_comentarios = soup_bug.find_all('pre', class_='bz_comment_text')

                    for comentario in soup_bug_comentarios:
                        soup_bug_comentario_texto = comentario.get_text()
                        match = re.search(r'BUG: ([kK][aA][sS][aA][nN]): (\S+)', soup_bug_comentario_texto)
                        
                        if match:
                            resultado = match.group(2)
                            break
                        else:
                            expresion_regular = re.search(r'kasan: GPF could be caused by (.*?)(?=general protection fault)', soup_bug_texto, re.DOTALL)
                            # Verificar si se encontró la cadena y extraerla
                            if expresion_regular:
                                resultado = expresion_regular.group(1)
                            else:
                                resultado = "No encontrado"
            '''

            # Obtener el texto que existe dentro de todo el texto.
            soup_bug_texto = str(soup_bug)

            # Utilizo una expresión regular para encontrar la palabra después de 'bug: KASAN:'
            match = re.search(r'BUG: ([kK][aA][sS][aA][nN]): (\S+)', soup_bug_texto)
            if match:
                resultado = match.group(2)
            else:
                expresion_regular = re.search(r'kasan: GPF could be caused by (.*?)(?=general protection fault)', soup_bug_texto, re.DOTALL)

                # Verificar si se encontró la cadena y extraerla
                if expresion_regular:
                    resultado = expresion_regular.group(1)
                else:
                    resultado = "No encontrado"
            
            # Encuentro el elemento de la tabla que contiene la fecha de cuando se hizo el reporte
            fila_reporte = soup_bug.find('tr', id='field_tablerow_reported')

            # Extraigo la fecha del reporte
            fecha = fila_reporte.find('td').get_text(strip=True)

            # Extraigo los últimos cuatro caracteres (año)
            anyo = fecha.split('-')[0]

            #Formar CVE.
            cve_final = "CVE-"+ anyo + "-" + bug_id

            #Buscar commit del usuario.
            # Buscar la etiqueta <table> con la clase 'bz_comment_table'
            etiqueta_commit = soup_bug.find('table', class_='bz_comment_table')

            # Verificar si se encontró la etiqueta y obtener el texto dentro de ella
            if etiqueta_commit:
                commit = etiqueta_commit.get_text("\n", strip=True)
            else:
                commit = "El usuario no subió ningún comentario"

            #Busco los adjuntos
            # Creamos una lista para almacenar las URLs de los archivos adjuntos
            url_adjuntos = []

            # Encuentro todos los elementos de la tabla de adjuntos
            filas_adjuntos = soup_bug.find_all('tr', class_=lambda x: x and 'bz_contenttype_' in x)

            # Itero sobre los elementos y extraigo las URLs de los archivos adjuntos
            for fila in filas_adjuntos:
                url_adjunto = fila.find('a', href=lambda x: x and 'attachment.cgi?id=' in x)['href']
                url_adjuntos.append(url_raiz_adjuntos+url_adjunto)

            # Convertir la lista de enlaces a una cadena separada por comas
            adjuntos_final = ', '.join(url_adjuntos)

            #Encontrar el tipo de hardware
            # Buscar la etiqueta <a> con el texto 'Hardware:' y luego obtener el siguiente <td>
            etiqueta_hardware = soup_bug.find('a', string='Hardware:')
            if etiqueta_hardware:
                hardware_info = etiqueta_hardware.find_next('td', class_='field_value')
                if hardware_info:
                    hardware = hardware_info.get_text(strip=True)
                else:
                    hardware = "No se encontró información de hardware."
            else:
                hardware = "No encontrado"
            
            #URL completa de Bugzilla
            url = url_raiz_adjuntos+bug_link
            
            # Insertar en la base de datos
            #cursor.execute('INSERT INTO bugs (tipo,cve,commit_mensaje,adjuntos,hardware,url) VALUES (?,?,?,?,?,?)', (resultado,cve_final,commit,adjuntos_final,hardware,url,))
            
            # Verificar si el CVE ya existe en la base de datos
            cursor.execute('SELECT cve FROM bugs WHERE cve = ?', (cve_final,))
            existe_cve = cursor.fetchone()

            if existe_cve is None:
                # Insertar en la base de datos solo si el CVE no existe
                cursor.execute('INSERT INTO bugs (tipo, cve, commit_mensaje, adjuntos, hardware, url) VALUES (?,?,?,?,?,?)',
                            (resultado, cve_final, commit, adjuntos_final, hardware, url,))
            else:
                print(f'El CVE {cve_final} ya existe en la base de datos. No se realizó la inserción.')
            
        else:
            print(f'Error al realizar la solicitud del bug: {respuesta.status_code}')

    # Commit y cerrar la conexión
    conn.commit()
    conn.close()
    

else:
    print(f'Error al realizar la solicitud: {respuesta.status_code}')