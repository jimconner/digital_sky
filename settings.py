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

# Define your preferred images here. These are used by the image_repeater and twinkle plugins. 
# If using voice control, the names here will need to match the words that Snips knows.
# Images will be saved with filename to match image name (i.e stars.jpg) to prevent repeated downloads.
# Here's some random starter images that look pretty. 
IMAGES={\
    'stars':'https://images-na.ssl-images-amazon.com/images/I/41J%2BOq%2B2zAL._SX355_.jpg', \
    'colours':'https://blog.radissonblu.com/wp-content/uploads/2017/03/The_impact_of_colors_image_1.jpg', \
    'sunset':'https://cdn-blog.queensland.com/wp-content/uploads/2014/08/garry-norris-main-beach-sunrise.jpg', \
    'sunrise': 'https://jordanrobins.com.au/wp-content/uploads/2017/12/Hyams-Beach-Sunrise-V1.2.jpg', \
    'rainbows': 'https://i.pinimg.com/originals/c4/48/72/c448728989cb84358d8bb1cacd4813e2.jpg', \
    'zigzag': 'https://media.paulsmith.com/media/catalog/product/r/n/rnsr-rugc-zigzag-1-detaila.jpg'
    }


