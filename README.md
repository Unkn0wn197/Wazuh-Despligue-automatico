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

Modificar el uso de menoria de java para dedicarle la necesaria.
```
sed -i 's/-Xms1g/-Xms4g/g' "/etc/elasticsearch/jvm.options"
sed -i 's/-Xmx1g/-Xmx4g/g' "/etc/elasticsearch/jvm.options"
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


### 3. Cambiar aspecto del panel gráfico con los iconos de la empresa(automatizar).
Cambiar logos de la gui principal. Descargar la carpeta assets de este github.
```
rm -rf /usr/share/kibana/plugins/wazuh/public/assets/
cp -R /home/bee/assets/ /usr/share/kibana/plugins/wazuh/public/
```


### 4. Integración de Wazuh con Telegram.
```
git clone https://github.com/Nicolceng/CustomTelegram.git
cd CustomTelegram
mv custom-telegram custom-telegram.py /var/ossec/integrations
chown root:ossec /var/ossec/integrations/custom-telegram*
chmod 750 /var/ossec/integrations/custom-telegram*
```

Introducimos el chatID con este comando para vincular el bot.
```
sed -i 's/CHAT_ID=""/CHAT_ID="key"/g' /var/ossec/integrations/custom-telegram.py
```

Pegamos este codigo dentro del archivo ossec.conf para la integración del bot. Importante cambiar la API KEY por la de nuestro Bot.
```
<integration>
  <name>custom-telegram</name>
  <level>3</level>
  <hook_url>https://api.telegram.org/bot*YOUR API KEY*/sendMessage</hook_url>
  <alert_format>json</alert_format>
</integration>
```


