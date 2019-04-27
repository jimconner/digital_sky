#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.cred import portal
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
from twisted.conch import avatar
from twisted.conch.checkers import SSHPublicKeyChecker, InMemorySSHKeyDB
from twisted.conch.ssh import factory, userauth, connection, keys, session
from twisted.conch.ssh.transport import SSHServerTransport
from twisted.internet import reactor, protocol
from twisted.python import log
from zope.interface import implementer
from twisted.conch import recvline
from numpy import uint8
import sys

class ExampleAvatar(avatar.ConchUser):
    """
    The avatar is used to configure SSH services/sessions/subsystems for
    an account.

    This account will use L{session.SSHSession} to handle a channel of
    type I{session}.
    """
    def __init__(self, username, datastore):
        avatar.ConchUser.__init__(self)
        self.datastore = datastore
        self.username = username
        self.channelLookup.update({b'session':session.SSHSession})

@implementer(portal.IRealm)
class ExampleRealm(object):
    """
    When using Twisted Cred, the pluggable authentication framework, the
    C{requestAvatar} method should return a L{avatar.ConchUser} instance
    as required by the Conch SSH server.
    """
    def __init__(self, datastore):
        self.datastore = datastore

    def requestAvatar(self, avatarId, mind, *interfaces):
        """
        See: L{portal.IRealm.requestAvatar}
        """
        return interfaces[0], ExampleAvatar(avatarId, self.datastore), lambda: None


class CLIProtocol(protocol.Protocol):
    def __init__(self, datastore):
        self.line=b''
        self.datastore=datastore

    def dataReceived(self, data):
        if data == b'\r':
            self.transport.write(b'\r\n')
            self.lineReceived(self.line)
            self.line=b''
        elif data == b'\x03': #^C
            self.transport.loseConnection()
            return
        self.line+=data    
        self.transport.write(data)

    def sendLine(self, line):
        self.transport.write(line+b'\r\n')

    def lineReceived(self, line):
        # Ignore blank lines
        if not line: return
        line = line.decode("ascii")

        # Parse the command
        commandParts = line.split()
        command = commandParts[0].lower()
        args = commandParts[1:]

        # Dispatch the command to the appropriate method.  Note that all you
        # need to do to implement a new command is add another do_* method.
        try:
            method = getattr(self, 'do_' + command)
        except AttributeError as e:
            self.sendLine(b'Error: no such command.')
            self.transport.write(b'$ ')
        else:
            try:
                method(*args)
                self.transport.write(b'$ ')
            except Exception as e:
                self.sendLine(b'Error: ' + str(e).encode("ascii"))
                self.transport.write(b'$ ')

    def do_help(self, command=None):
        """help [command]: List commands, or show help on the given command"""
        if command:
            doc = getattr(self, 'do_' + command).__doc__
            self.sendLine(doc.encode("ascii"))
        else:
            commands = [cmd[3:].encode("ascii")
                        for cmd in dir(self)
                        if cmd.startswith('do_')]
            self.sendLine(b"Valid commands: " + b" ".join(commands))

    def do_quit(self):
        """quit: Quit this session"""
        self.sendLine(b'Goodbye.')
        self.transport.loseConnection()        

    def do_plugins(self):
          """List the available plugins"""
          for plugin in self.datastore.plugins:
            self.sendLine(str(plugin.__name__).encode()[8:])
    def do_plugins(self):
          """List the available plugins"""
          for plugin in self.datastore.plugins:
            self.sendLine(str(plugin.__name__).encode()[8:])

    def do_animations(self):
          """List running animations"""
          self.sendLine(b'RGB Animations')
          for animation in self.datastore.animations:
              self.sendLine(str(animation.__module__[8:]).encode())
          self.sendLine(b'Strip Animations')
          for animation in self.datastore.strip_animations:
              self.sendLine(str(animation.__module__[8:]).encode())

    def do_add(self, pluginname, extra=None, extra2=None):
          """ Add an instance of a plugin to the running animations list"""
          self.datastore.add_animation(pluginname, extra, extra2)
                  	
    def do_del(self, pluginname):
          """ Add an instance of a plugin to the running animations list"""
          self.datastore.del_animation(pluginname)

    def do_nw(self, val):
        """Set level if Natural White strips (0-255)"""
        self.datastore.strip_vals[0]=uint8(val)

    def do_dw(self, val):
        """Set level if Daylight White strips (0-255)"""
        self.datastore.strip_vals[1]=uint8(val)

    def do_ib(self, val):
        """Set level if Ice Blue strips (0-255)"""
        self.datastore.strip_vals[2]=uint8(val)

    def do_ww(self, val):
        """Set level if Warm White strips (0-255)"""
        self.datastore.strip_vals[3]=uint8(val)
        
    def do_lightsout(self):
        """Stop all animations and turn all lights off"""
        self.strip_vals = [0,0,0,0]
        self.datastore.animations=[]
        self.datastore.strip_animations=[]
        self.datastore.add_animation("set_strips")
        
    def do_brt(self, val):
        """Set the master brightness. Range: 0.00-1.00"""
        self.datastore.master_brightness=float(val)
    def do_brtr(self, val):
        """Set the brightness for the Red channel. Range: 0.00-1.00"""
        self.datastore.rgbw_brightness[0]=float(val)
    def do_brtg(self, val):
        """Set the brightness for the Green channel. Range: 0.00-1.00"""
        self.datastore.rgbw_brightness[1]=float(val)
    def do_brtb(self, val):
        """Set the brightness for the Blue channel. Range: 0.00-1.00"""
        self.datastore.rgbw_brightness[2]=float(val)        
    def do_brtw(self, val):
        """Set the brightness for the White channel. Range: 0.00-1.00"""
        self.datastore.rgbw_brightness[3]=float(val)

class ExampleSession(object):
    def __init__(self, avatar):
        """
        In this example the avatar argument is not used for session selection,
        but for example you can use it to limit I{shell} or I{exec} access
        only to specific accounts.
        """
        self.datastore = avatar.datastore
  
    def getPty(self, term, windowSize, attrs):
        """
        We don't support pseudo-terminal sessions.
        """

    def execCommand(self, proto, cmd):
        """
        We don't support command execution sessions.
        """
        raise Exception("not executing commands")

    def openShell(self, transport):
        """
        Use our protocol as shell session.
        """
        protocol = CLIProtocol(self.datastore)
        # Connect the new protocol to the transport and the transport
        # to the new protocol so they can communicate in both directions.
        protocol.makeConnection(transport)
        transport.makeConnection(session.wrapProtocol(protocol))
        protocol.transport.write(b'Welcome to Digital Sky\r\nType "help" for help.\r\n$ ')


    def eofReceived(self):
        pass

    def closed(self):
        pass


