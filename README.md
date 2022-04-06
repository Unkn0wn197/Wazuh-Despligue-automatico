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
