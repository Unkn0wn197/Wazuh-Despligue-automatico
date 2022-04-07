# Wazuh Despligue automatico.
Desarrollo de un script para automatizar el despligue de un SOC.


### Adquisición de Cloud. 
Preferiblemente Centos. Mínimo 8 Gb de RAM y un par de Cores.


### 1. Instalacion de Wazuh por script.
Verificar que es la última versión.
```
curl -so ~/unattended-installation.sh https://packages.wazuh.com/resources/4.2/open-distro/unattended-installation/unattended-installation.sh && bash ~/unattended-installation.sh
```
Anotar las credenciales que salen al final de la instalación ya que no vuelven a salir nunca más.


### 2. Configuraciones extras para el sistema.
Bloquear memoria de elastic para que no sobrecargue el sistema. Añadir esta linea al final del archivo (/etc/elasticsearch/elasticsearch.ym).
```
bootstrap.memory_lock: true
```

Modificar el uso de menoria de java para dedicarle la necesaria. Añadir estas lineas al archivo (/etc/elasticsearch/jvm.options).
```
-Xms4g 
-Xmx4g
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
### 3. Cambiar aspecto del panel gráfico con los iconos de la empresa.
Cambiar logos de la gui principal(sustituir carpeta assets por la otra).
```
https://github.com/ramsal/ProtocolosTecnicos/blob/master/Wazuh/assets.zip) en la carpeta /usr/share/kibana/plugins/wazuh/public/assets/
```
### 4. Integración de Wazuh con Telegram.
git clone https://github.com/Nicolceng/CustomTelegram.git
```
```
cd CustomTelegram

mv custom-telegram custom-telegram.py /var/ossec/integrations
```
chown root:ossec /var/ossec/integrations/custom-telegram*
```
chmod 750 /var/ossec/integrations/custom-telegram*
```
nano custom-telegram.py
```
Dentro de custom-telegram.py editar la variable de chat_id por el chat_id de nuestro bot

nano /var/ossec/etc/ossec.conf
```
Pegar dentro del archivo ossec.conf la siguiente integración:

<integration>
  <name>custom-telegram</name>
  <level>3</level>
  <hook_url>https://api.telegram.org/bot*YOUR API KEY*/sendMessage</hook_url>
  <alert_format>json</alert_format>
</integration>






