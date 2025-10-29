# M3U Source

Servicio web Flask para modificar archivos de playlist M3U, reemplazando direcciones localhost por hosts personalizados y convirtiendo enlaces acestream a formato HTTP.

## Funcionalidad

- **Reemplazo de localhost**: Convierte `http://127.0.0.1:puerto` y `http://localhost:puerto` por tu `host:port` personalizado
- **Conversión acestream**: Transforma URLs `acestream://[id]` a formato HTTP `http://host:port/ace/getstream?id=[id]`

## Uso

### Endpoint

```
GET /modify_m3u
```

### Parámetros

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `m3u_url` | string | Sí | URL del archivo M3U a modificar |
| `host` | string | Sí | Host de destino (hostname o IP) |
| `port` | integer | Sí | Puerto de destino (1-65535) |

### Ejemplo

```bash
curl "http://localhost:5000/modify_m3u?m3u_url=http://ejemplo.com/playlist.m3u&host=192.168.1.100&port=6878" \
  -o modified_playlist.m3u
```

## Instalación

### Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
```

La aplicación estará disponible en `http://0.0.0.0:5000`

### Docker

```bash
# Construir imagen
docker build -t m3usource .

# Ejecutar contenedor
docker run -p 5000:5000 m3usource
```

### GitHub Container Registry

```bash
docker pull ghcr.io/krinkuto11/m3usource:latest
docker run -p 5000:5000 ghcr.io/krinkuto11/m3usource:latest
```

## Dependencias

- Flask 2.2.2
- requests 2.28.1
- Werkzeug 2.2.2

## Notas

- Para producción, usar un servidor WSGI como gunicorn o uwsgi
- Los IDs de acestream deben ser hashes válidos de 40 caracteres hexadecimales
- El timeout de descarga de M3U es de 15 segundos
