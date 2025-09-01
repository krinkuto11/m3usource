from flask import Flask, jsonify
import requests

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
    modified_content = content.replace('http://127.0.0.1:6878/', 'http://127.0.0.1:8080/')
    return modified_content

@app.route('/modify_m3u', methods=['GET'])
def modify_m3u():
    # URL del archivo M3U
    m3u_url = 'http://example.com/playlist.m3u'  # Cambia esto por la URL de tu archivo M3U

    m3u_content = get_m3u_content(m3u_url)

    if m3u_content:
        modified_content = modify_m3u_content(m3u_content)
        return jsonify({'status': 'success', 'modified_m3u': modified_content})
    else:
        return jsonify({'status': 'error', 'message': 'No se pudo descargar el archivo M3U'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

