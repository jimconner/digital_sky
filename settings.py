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


#STARTUP_SCRIPT="""
#add set_strips
#add twinkle https://images-na.ssl-images-amazon.com/images/I/41J%2BOq%2B2zAL._SX355_.jpg 3
#"""

