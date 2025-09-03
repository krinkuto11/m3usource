from flask import Flask, send_file
import requests
import io

app = Flask(__name__)

# Función para descargar el archivo M3U desde la URL
def get_m3u_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Función para modificar el contenido del M3U
def modify_m3u_content(content):
    modified_content = content.replace('http://127.0.0.1:6878/', 'http://acexy:8080/')
    return modified_content

@app.route('/modify_m3u', methods=['GET'])
def modify_m3u():
    # URL del archivo M3U
    m3u_url = 'http://192.168.20.3:43110/1JKe3VPvFe35bm1aiHdD4p1xcGCkZKhH3Q/data/listas/lista_iptv.m3u'  # Cambia esto por la URL de tu archivo M3U

    m3u_content = get_m3u_content(m3u_url)

    if m3u_content:
        modified_content = modify_m3u_content(m3u_content)
        
        # Convertimos el contenido modificado a un objeto de archivo en memoria
        modified_file = io.BytesIO(modified_content.encode('utf-8'))        
        # Devolvemos el archivo modificado como respuesta
        return send_file(
            modified_file,
            mimetype='application/x-mpegURL',  # Tipo MIME adecuado para archivos M3U
            as_attachment=True,
            download_name='modified_playlist.m3u'
        )
    else:
        return "No se pudo descargar el archivo M3U", 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
