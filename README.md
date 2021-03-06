# Wazuh Despligue automatico.
Desarrollo de un script para automatizar el despligue de un SOC.


### 1. Instalacion de Wazuh por script.
Instalar dependencias necesarias.
```
apt install gnupg curl git -y
```

Verificar que es la última versión.
```
curl -so ~/unattended-installation.sh https://packages.wazuh.com/resources/4.2/open-distro/unattended-installation/unattended-installation.sh && bash ~/unattended-installation.sh
```
Anotar las credenciales que salen al final de la instalación ya que no vuelven a salir nunca más.


### 2. Configuraciones extras para el sistema.
Bloquear memoria de elastic para que no sobrecargue el sistema.
```
echo 'bootstrap.memory_lock: true' >> /etc/elasticsearch/elasticsearch.yml
```

Modificar el uso de menoria de java para dedicarle la necesaria(4gb en este caso).
```
sed -i 's/-Xms1g/-Xms4g/g' "/etc/elasticsearch/jvm.options" && sed -i 's/-Xmx1g/-Xmx4g/g' "/etc/elasticsearch/jvm.options"
```

Editar los limites de recursos del sistema.
```
mkdir -p /etc/systemd/system/elasticsearch.service.d/
```
```
cat > /etc/systemd/system/elasticsearch.service.d/elasticsearch.conf << EOF
[Service]
LimitMEMLOCK=infinity
EOF
```


### 3. Descargamos los recursos necesarios.
Antes de continuar tendremos que descargar la carpeta recursos de este github en la carpeta de usuario de la maquina.


### 4. Cambiar aspecto del panel gráfico con los iconos de la empresa(automatizar).
Cambiar logos de la gui principal. Descargar la carpeta assets de este github.
```
rm -rf /usr/share/kibana/plugins/wazuh/public/assets/
cp -R /home/bee/recursos/assets/ /usr/share/kibana/plugins/wazuh/public/
```
Cambiar aspecto del Login
```
echo 'opendistro_security.basicauth.login.brandimage: "https://beehackers.es/wp-content/uploads/2018/04/BH.png"' >> /etc/kibana/kibana.yml
echo 'opendistro_security.basicauth.login.title: SOC OMNICANAL' >> /etc/kibana/kibana.yml
echo 'opendistro_security.basicauth.login.subtitle: Omnichannel Security Operations Center' >> /etc/kibana/kibana.yml
```


### 5. Integración de Wazuh con VirusTotal.
Pegamos este código dentro del archivo ossec.conf.
```
  <!-- INTEGRATION WITH VIRUSTOTAL================================================================================= -->
  <integration>
    <name>virustotal</name>
    <api_key>API_KEY</api_key> <!-- Replace with your VirusTotal API key -->
    <group>syscheck</group>
    <alert_format>json</alert_format>
  </integration>
```


### 6. Integración de Wazuh con Telegram.
```
cd /home/bee/recursos
mv custom-telegram custom-telegram.py /var/ossec/integrations
chown root:ossec /var/ossec/integrations/custom-telegram*
chmod 750 /var/ossec/integrations/custom-telegram*
```

Introducimos estos comandos para poner la chatID y la key del bot(Sustituir keyBot por la id del bot y keyChat por la id del chat).
```
sed -i 's/BOT_ID="KEYBOTID"/BOT_ID="keyBot"/g' /var/ossec/integrations/custom-telegram.py
sed -i 's/CHAT_ID="KEYCHATID"/CHAT_ID="keyChat"/g' /var/ossec/integrations/custom-telegram.py
```

Pegamos este código dentro del archivo ossec.conf para la integración del bot (Sustituir APIKEY por la de nuestro bot).
```
<!-- INTEGRATION WITH TELEGRAM=================================================================================== -->
<integration>
  <name>custom-telegram</name>
  <level>3</level>
  <hook_url>https://api.telegram.org/botAPIKEY/sendMessage</hook_url>
  <alert_format>json</alert_format>
</integration>
```
