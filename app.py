from flask import Flask, send_file, request, abort
import requests
import io
import re

app = Flask(__name__)

DEFAULT_M3U_URL = 'http://192.168.20.3:43110/1JKe3VPvFe35bm1aiHdD4p1xcGCkZKhH3Q/data/listas/lista_iptv.m3u'

# Descarga el archivo M3U desde la URL
def get_m3u_content(url):
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        app.logger.error(f"Error descargando M3U: {e}")
        return None

# Valida host y port
HOST_REGEX = re.compile(r'^[a-zA-Z0-9\.\-]+$')  # hostname o IPv4 simple
def validate_host_port(host, port_str):
    if not host or not HOST_REGEX.match(host):
        return False, "Parámetro 'host' inválido."
    try:
        port = int(port_str)
        if not (1 <= port <= 65535):
            return False, "Parámetro 'port' fuera de rango (1-65535)."
    except (TypeError, ValueError):
        return False, "Parámetro 'port' debe ser un entero."
    return True, port

# Modifica el contenido del M3U reemplazando 127.0.0.1/localhost:<puerto> por host:port
def modify_m3u_content(content, host, port):
    # Sustituye sólo el prefijo del URL (mantiene el path que venga después)
    # Coincide con http://127.0.0.1:<puerto>... o http://localhost:<puerto>...
    pattern = re.compile(r'http://(?:127\.0\.0\.1|localhost):\d+(?=/)')
    replacement = f'http://{host}:{port}'
    modified = pattern.sub(replacement, content)
    return modified

@app.route('/modify_m3u', methods=['GET'])
def modify_m3u():
    # Lee parámetros de query
    host = request.args.get('host', '').strip()
    port_str = request.args.get('port', '').strip()
    m3u_url = (request.args.get('m3u_url') or DEFAULT_M3U_URL).strip()

    ok, port_or_msg = validate_host_port(host, port_str)
    if not ok:
        return port_or_msg, 400
    port = port_or_msg

    m3u_content = get_m3u_content(m3u_url)
    if not m3u_content:
        return "No se pudo descargar el archivo M3U", 400

    modified_content = modify_m3u_content(m3u_content, host, port)

    # Devuelve el archivo modificado
    modified_file = io.BytesIO(modified_content.encode('utf-8'))
    return send_file(
        modified_file,
        mimetype='application/x-mpegURL',
        as_attachment=True,
        download_name='modified_playlist.m3u'
    )

if __name__ == '__main__':
    # Producción: usa un WSGI (gunicorn/uwsgi). Esto es sólo para desarrollo.
    app.run(debug=True, host='0.0.0.0', port=5000)
