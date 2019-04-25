from twisted.logger   import (
    LogLevel, LogLevelFilterPredicate)

# Settings file for digital_sky
    
    
LED_COUNT=469 # Total number of addressable pixels (including virtual pixels with strips attached)
LAMP_LENGTH=67 # The lenth of each lamp module
STRIP_LEDS=3 # The number of virtual pixels (with strips attached) at the start of each lamp.

# ----------------
# Global variables
# ----------------

# Global object to control globally namespace logging
logLevelFilterPredicate = LogLevelFilterPredicate(defaultLogLevel=LogLevel.info)

# MQTT Service to subscribe to
BROKER = "tcp:localhost:1883"


# Path to RSA SSH keys used by the server. (generate them with ssh-keygen and put them in the folder)
SERVER_RSA_PRIVATE = 'ssh-keys/ssh_host_rsa_key'
SERVER_RSA_PUBLIC = 'ssh-keys/ssh_host_rsa_key.pub'

# Path to RSA SSH keys accepted by the server (copy the id_rsa.pub key(s) of users you permit into this file)
CLIENT_RSA_PUBLIC = 'ssh-keys/client_rsa.pub'


#STARTUP_SCRIPT="""
#add set_strips
#add twinkle https://images-na.ssl-images-amazon.com/images/I/41J%2BOq%2B2zAL._SX355_.jpg 3
#"""

