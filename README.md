# M3U Source

Servicio web Flask para modificar archivos de playlist M3U, reemplazando direcciones localhost por hosts personalizados y convirtiendo enlaces acestream a formato HTTP.

## Funcionalidad

- **Reemplazo de localhost** (modo por defecto): Convierte `http://127.0.0.1:puerto` y `http://localhost:puerto` por tu `host:port` personalizado
- **Conversión acestream** (modo por defecto): Transforma URLs `acestream://[id]` a formato HTTP `http://host:port/ace/getstream?id=[id]`
- **Modo proxy**: Reescribe todas las URLs en formato `http://host:port/proxy/<url_original>` para enrutar todo el tráfico a través de un servidor proxy

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
| `mode` | string | No | Modo de operación: `default` o `proxy` (por defecto: `default`) |

### Ejemplo

#### Modo por defecto (reemplazo de localhost y conversión acestream)

```bash
curl "http://localhost:5000/modify_m3u?m3u_url=http://ejemplo.com/playlist.m3u&host=192.168.1.100&port=6878" \
  -o modified_playlist.m3u
```

#### Modo proxy (todas las URLs a través de proxy)

```bash
curl "http://localhost:5000/modify_m3u?m3u_url=http://ejemplo.com/playlist.m3u&host=192.168.1.100&port=8080&mode=proxy" \
  -o modified_playlist.m3u
```

Este modo reescribe URLs como:
- Original: `http://provider.com/stream/123.ts`
- Reescrita: `http://192.168.1.100:8080/proxy/http://provider.com/stream/123.ts`

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

## Configuración

### Variables de entorno

- `M3U_TIMEOUT` (float): define cuántos segundos espera la aplicación al descargar el archivo M3U. Si no se configura toma el valor por defecto de 15. Una vez que se inicia la app con este valor, se puede seguir ajustando en cada petición usando el parámetro `timeout`.

Ejemplo para cambiarlo en local:

```bash
M3U_TIMEOUT=30 python app.py
```

Ejemplo con Docker:

```bash
docker run -p 5000:5000 -e M3U_TIMEOUT=30 m3usource
```

## Notas

- Para producción, usar un servidor WSGI como gunicorn o uwsgi
- Los IDs de acestream deben ser hashes válidos de 40 caracteres hexadecimales
- El timeout de descarga de M3U es de 15 segundos
