
# Bender

#### Bot controlador y generador de contenido para YouTube

# Requerimientos

## FFMPEG

Debian 9 "Stretch"

```sh
sudo apt-get update
```

```sh
sudo apt-get install ffmpeg
```

## MONGODB

```sh
sudo apt-get update
```

```sh
sudo apt-get install mongodb
```

### Crear usuario admin en Mongo (no seas zapallo/a y SIEMPRE que puedas restringí con credenciales tu BD)

```sh
mongo
```

```sh
use admin
```

```javascript
db.createUser(
{
    user: "admin",
    pwd: "<pass_db>",
    roles: [
              { role: "userAdminAnyDatabase", db: "admin" },
              { role: "readWriteAnyDatabase", db: "admin" },
              { role: "dbAdminAnyDatabase", db: "admin" },
              { role: "clusterAdmin", db: "admin" }
           ]
})
```

### Setear Auth

```sh
nano /etc/mongod.conf
```

```sh
nano /etc/mongodb.conf
```

```sh
auth = true
```

```sh
service mongodb restart
```

### En caso de recuperar backup.

Mover archivos a:

```
/var/lib/mongodb
```

```sh
sudo rm /var/lib/mongodb/mongod.lock
```

```sh
sudo chown -R mongodb:mongodb /var/lib/mongodb*
```

```sh
service mongodb restart
```

### Instalar dependencias necesarias.

```sh
pip install -r requirements.txt
```

### Google API

Ingresar a Google Developer Console:

```
https://console.developers.google.com/apis
```

Habilitar Youtube Data API v3

### Crear archivo de autenticación para subir video a YouTube

Una vez habilitada la API en el paso anterior, en la sección credenciales, se debe habilitar un "ID de cliente OAuth 2.0" y bajar el archivo  client_secrets.json que te genera y guardarlo en la raíz del proyecto junto con el archivo `oauth.py`

Luego se debe ejecutar (en un entorno gráfico, porque se encesita el browser)

```sh
python oauth.py
```

Este comando abrirá el navegador donde deberás seleccionar (estando previamente logueado con la cuenta de Google que utilizarás) el canal de YouTube al que autorizas la API.

Si todo sale bien, de deberá crear en la raíz del proyecto un archivo `api-oauth2.json`

### Setear variables en globals.py

Abrir el archivo `globals.py` y cambiar los siguientes valores.

```
9  'password': '<db_password>', #Password de la BD Mongo.
```

```
44 YOUTUBE_CHANNEL_ID = "<channel_id>" #ID del canal del bot.
```

```
45 YOUTUBE_API_KEY = "<google_api_key>" #API Key de Google Developer Console en la seccion credenciales (se usa para recuperar tags y estadíticas)
```

En el caso de usar un bot de telegram para informar estadísticas y subidas de video:

```
60 BOT_TELEGRAM_TOKEN = "<bot_telegram_token>" #Token del bot creado en telegram.
```

```
61 BOT_TELEGRAM_CHAT_ID = "<id_chat_bot>" #ID del chat generado con el bot para que pueda enviar los datos.
```

El envio a bot de Telegram está deshabilitado pero se puede activar descomentando las correspondientes lineas.


### Crear servicio con servidor flask.

```sh
nano /etc/init.d/flask
```

**Cambiar [USER] por el correspondiente nombre de usuario.**

```sh
#! /bin/sh
### BEGIN INIT INFO
# Provides:          flask
# Required-Start:    $all
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:
# Short-Description: Servidor Bender
### END INIT INFO 

NAME=flask
DESC="Demonio del servidor Bender"
PIDFILE="/var/run/${NAME}.pid"
LOGFILE="/var/log/${NAME}.log"

DAEMON="/usr/bin/python"
#Ruta del archivo
DAEMON_OPTS="/home/[USER]/bender/server.py"
 
START_OPTS="--start --background --make-pidfile --pidfile ${PIDFILE} --exec ${DAEMON} ${DAEMON_OPTS}"
STOP_OPTS="--stop --pidfile ${PIDFILE}"
 
test -x $DAEMON || exit 0
 
set -e
 
case "$1" in
    start)
        echo -n "Starting ${DESC}: "
        start-stop-daemon $START_OPTS >> $LOGFILE
        echo "$NAME."
        ;;
    stop)
        echo -n "Stopping $DESC: "
        start-stop-daemon $STOP_OPTS
        echo "$NAME."
        rm -f $PIDFILE
        ;;
    restart|force-reload)
        echo -n "Restarting $DESC: "
        start-stop-daemon $STOP_OPTS
        sleep 1
        start-stop-daemon $START_OPTS >> $LOGFILE
        echo "$NAME."
        ;;
    *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop|restart|force-reload}" >&2
        exit 1
        ;;
esac
 
exit 0
```

```sh
chmod +x /etc/init.d/nombre_servicio
```

#### Autoarranque

```sh
/lib/systemd/systemd-sysv-install enable flask
```

### Instalar gnome-shcedule (en el caso de que se monte en Raspbian)

```sh
/lib/systemd/systemd-sysv-install enable flask
```

### Crear crons

```sh
sudo apt-get install gnome-schedule
```

**Cambiar [USER] por el correspondiente nombre de usuario.**

```sh
#BENDER CRONS
#Estadisticas (08:10)
10 08 * * * [USER] /usr/bin/python /home/[USER]/bender/core.py r2d2
#Minado Contenido (19:15)
15 19 * * * [USER] /usr/bin/python /home/[USER]/bender/core.py walle
#Produccion y subida (21:30)
30 21 * * * [USER] /usr/bin/python /home/[USER]/bender/core.py optimus
```





ˁ(⦿ᴥ⦿)ˀ RnVjayB0aGUgcnVsZXMh
