import sys, json

from twisted.internet.defer       import inlineCallbacks, DeferredList
from twisted.internet             import reactor
from twisted.internet.endpoints   import clientFromString
from twisted.application.internet import ClientService, backoffPolicy


from mqtt.client.factory import MQTTFactory


# -----------------------
# MQTT Subscriber Service
# ------------------------

class MQTTService(ClientService):


    def __init__(self, endpoint, factory, log, datastore):
        self.log=log
        self.datastore=datastore
        ClientService.__init__(self, endpoint, factory, retryPolicy=backoffPolicy())


    def startService(self):
        self.log.info("starting MQTT Client Subscriber Service")
        # invoke whenConnected() inherited method
        self.whenConnected().addCallback(self.connectToBroker)
        ClientService.startService(self)


    @inlineCallbacks
    def connectToBroker(self, protocol):
        '''
        Connect to MQTT broker
        '''
        self.protocol                 = protocol
        self.protocol.onPublish       = self.onPublish
        self.protocol.onDisconnection = self.onDisconnection
        self.protocol.setWindowSize(3) 
        try:
            yield self.protocol.connect("TwistedMQTT-subs", keepalive=60)
            yield self.subscribe()
        except Exception as e:
            self.log.error("Connecting to {broker} raised {excp!s}", 
               broker=BROKER, excp=e)
        else:
            self.log.info("Connected and subscribed to broker")


    def subscribe(self):

        def _logFailure(failure):
            self.log.debug("reported {message}", message=failure.getErrorMessage())
            return failure

        def _logGrantedQoS(value):
            self.log.debug("response {value!r}", value=value)
            return True

        def _logAll(*args):
            self.log.debug("all subscriptions complete args={args!r}",args=args)
            
        d1 = self.protocol.subscribe("hermes/hotword/default/detected", 2 )
        d1.addCallbacks(_logGrantedQoS, _logFailure)

        d2 = self.protocol.subscribe("hermes/intent/#", 2 )
        d2.addCallbacks(_logGrantedQoS, _logFailure)

        d3 = self.protocol.subscribe("foo/bar/baz3", 2 )
        d3.addCallbacks(_logGrantedQoS, _logFailure)

        dlist = DeferredList([d1,d2,d3], consumeErrors=True)
        dlist.addCallback(_logAll)
        return dlist


    def onPublish(self, topic, payload, qos, dup, retain, msgId):
        '''
        Callback Receiving messages from publisher
        '''
        self.log.debug("msg={payload}", payload=payload)
        try:
            payload=json.loads(str(payload, 'utf-8', 'ignore'))
        except:
            print("*** Explodey Death thing when processing message from mqtt ***")
            print(payload)
        if topic == 'hermes/hotword/default/detected':
            print("Snips is listening")
            self.datastore.add_animation('pulse')
        if topic == 'hermes/intent/jimconner:natural':
            print("Natural White")
            self.datastore.strip_vals[0]=int(payload['slots'][0]['value']['value']*2.55)
        if topic == 'hermes/intent/jimconner:daylight':
            self.log.info("Daylight White")
            self.datastore.strip_vals[1]=int(payload['slots'][0]['value']['value']*2.55)
        if topic == 'hermes/intent/jimconner:blue':
            self.log.info("Ice Blue")
            self.datastore.strip_vals[2]=int(payload['slots'][0]['value']['value']*2.55)
        if topic == 'hermes/intent/jimconner:warm':
            self.log.info("Warm White")
            self.datastore.strip_vals[3]=int(payload['slots'][0]['value']['value']*2.55)
        if topic == 'hermes/intent/jimconner:lights_off':
            self.log.info("Lights Off")
            self.datastore.strip_vals=[0,0,0,0]
            self.datastore.animations=[]
            self.datastore.strip_animations=[]
            self.datastore.add_animation("set_strips")
        if topic == 'hermes/intent/jimconner:add':
            self.log.info("Add a thing")
            if len(payload['slots']) == 1:
                self.datastore.add_animation(payload['slots'][0]['value']['value'])
            elif len(payload['slots']) == 2:
                self.datastore.add_animation(payload['slots'][0]['value']['value'],payload['slots'][1]['value']['value'])
            elif len(payload['slots']) == 3:
                self.datastore.add_animation(payload['slots'][0]['value']['value'],payload['slots'][1]['value']['value'],payload['slots'][2]['value']['value'])
            else:
                print('Can only process adding things with 1-3 slots. Code changes needed for anything else.')
        if topic == 'hermes/intent/jimconner:delete':
            self.log.info("Delete a thing")
            self.datastore.del_animation(payload['slots'][0]['value']['value'])
        if topic == 'hermes/intent/jimconner:brightness':
            if len(payload['slots']) == 1:
                self.datastore.master_brightness=float(payload['slots'][0]['value']['value']/100)
            else:
                print("Slots Length:", len(payload['slots']))
                for slot in range(len(payload['slots'])):
                    print(payload['slots'][slot])
                if payload['slots'][0]['value']['value'] == 'red':
                    self.datastore.rgbw_brightness[0]=float(payload['slots'][1]['value']['value']/100)
                if payload['slots'][0]['value']['value'] == 'green':
                    self.datastore.rgbw_brightness[1]=float(payload['slots'][1]['value']['value']/100)
                if payload['slots'][0]['value']['value'] == 'blue':
                    self.datastore.rgbw_brightness[2]=float(payload['slots'][1]['value']['value']/100)
                if payload['slots'][0]['value']['value'] == 'white':
                    self.datastore.rgbw_brightness[3]=float(payload['slots'][1]['value']['value']/100)
                if payload['slots'][0]['value']['value'] == 'master':
                    self.datastore.master_brightness=float(payload['slots'][0]['value']['value']/100)
                print(self.datastore.rgbw_brightness)
                        


    def onDisconnection(self, reason):
        '''
        get notfied of disconnections
        and get a deferred for a new protocol object (next retry)
        '''
        self.log.debug("<Connection was lost !> <reason={r}>", r=reason)
        self.whenConnected().addCallback(self.connectToBroker)


if __name__ == '__main__':
    import sys
    log = Logger()
    startLogging()
    setLogLevel(namespace='mqtt',     levelStr='debug')
    setLogLevel(namespace='__main__', levelStr='debug')

    factory    = MQTTFactory(profile=MQTTFactory.SUBSCRIBER)
    myEndpoint = clientFromString(reactor, BROKER)
    serv       = MQTTService(myEndpoint, factory)
    serv.startService()
    reactor.run()
    
