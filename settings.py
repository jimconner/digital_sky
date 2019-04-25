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


# Path to RSA SSH keys used by the server.
SERVER_RSA_PRIVATE = 'ssh-keys/ssh_host_rsa_key'
SERVER_RSA_PUBLIC = 'ssh-keys/ssh_host_rsa_key.pub'

# Path to RSA SSH keys accepted by the server.
CLIENT_RSA_PUBLIC = 'ssh-keys/client_rsa.pub'


# Pre-computed big prime numbers used in Diffie-Hellman Group Exchange as
# described in RFC4419.
# This is a short list with a single prime member and only for keys of size
# 1024 and 2048.
# You would need a list for each SSH key size that you plan to support in your
# server implementation.
# You can use OpenSSH ssh-keygen to generate these numbers.
# See the MODULI GENERATION section from the ssh-keygen man pages.
# See moduli man pages to find out more about the format used by the file
# generated using ssh-keygen.
# For Conch SSH server we only need the last 3 values:
# * size
# * generator
# * modulus
#
# The format required by the Conch SSH server is:
#
# {
#   size1: [(generator1, modulus1), (generator1, modulus2)],
#   size2: [(generator4, modulus3), (generator1, modulus4)],
# }
#
# twisted.conch.openssh_compat.primes.parseModuliFile provides a parser for
# reading OpenSSH moduli file.
#
# Warning! Don't use these numbers in production.
# Generate your own data.
# Avoid 1024 bit primes https://weakdh.org
#


PRIMES = {
    2048: [(2, 24265446577633846575813468889658944748236936003103970778683933705240497295505367703330163384138799145013634794444597785054574812547990300691956176233759905976222978197624337271745471021764463536913188381724789737057413943758936963945487690939921001501857793275011598975080236860899147312097967655185795176036941141834185923290769258512343298744828216530595090471970401506268976911907264143910697166165795972459622410274890288999065530463691697692913935201628660686422182978481412651196163930383232742547281180277809475129220288755541335335798837173315854931040199943445285443708240639743407396610839820418936574217939)],
    4096: [(2, 889633836007296066695655481732069270550615298858522362356462966213994239650370532015908457586090329628589149803446849742862797136176274424808060302038380613106889959709419621954145635974564549892775660764058259799708313210328185716628794220535928019146593583870799700485371067763221569331286080322409646297706526831155237865417316423347898948704639476720848300063714856669054591377356454148165856508207919637875509861384449885655015865507939009502778968273879766962650318328175030623861285062331536562421699321671967257712201155508206384317725827233614202768771922547552398179887571989441353862786163421248709273143039795776049771538894478454203924099450796009937772259125621285287516787494652132525370682385152735699722849980820612370907638783461523042813880757771177423192559299945620284730833939896871200164312605489165789501830061187517738930123242873304901483476323853308396428713114053429620808491032573674192385488925866607192870249619437027459456991431298313382204980988971292641217854130156830941801474940667736066881036980286520892090232096545650051755799297658390763820738295370567143697617670291263734710392873823956589171067167839738896249891955689437111486748587887718882564384870583135509339695096218451174112035938859)],
    }


#STARTUP_SCRIPT="""
#add set_strips
#add twinkle https://images-na.ssl-images-amazon.com/images/I/41J%2BOq%2B2zAL._SX355_.jpg 3
#"""

