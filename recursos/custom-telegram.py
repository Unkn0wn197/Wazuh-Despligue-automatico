import sys
import json
import requests
from requests.auth import HTTPBasicAuth


#Configuracion de parametros.
BOT_ID="KEYBOTID"#ID del bot
CHAT_ID="KEYCHATID"#ID del chat donde enviara los mensajes
alert_file = open(sys.argv[1])#Archivo que contiene las alertas de wazuh.


#Lectura del archivo de alertas.
alert_json = json.loads(alert_file.read())
alert_file.close()


#Extraer campos de datos.
alert_level = alert_json['rule']['level'] if 'level' in alert_json['rule'] else "N/A"
description = alert_json['rule']['description'] if 'description' in alert_json['rule'] else "N/A"
agent = alert_json['agent']['name'] if 'name' in alert_json['agent'] else "N/A"


#Funcion para enviar los mensajes y estructurarlos
def enviarMensaje(agent, description):
    message = "AGENTE: "+agent+" ALERTA: "+description
    requests.post('https://api.telegram.org/bot' + BOT_ID + '/sendMessage',
        data={'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'HTML'})


#Filtro para que saque solo estos mensajes
if "New dpkg" in description:
   enviarMensaje(agent, description)

elif "Listened ports status (netstat) changed" in description:
   enviarMensaje(agent, description)

elif "14" == str(alert_level):
   enviarMensaje(agent, description)


sys.exit(0)
