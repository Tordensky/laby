# -*- coding: utf-8 -*-

# Message protocol class.

import socket as s
from message import *

class protocolBase:
    """ Protocol for transferring messages 
        between peers in simple applications. """
    
    def __init__(self):
        """ Initializes a socket for connecting to a peers. """
        
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.conn = sock
        
        # Bool for connection status
        self.CONNECTED = False
        
    def connect(self, host, port):
        """ Connect to a peer with given hostname and port. """
       
        if self.CONNECTED == False: 
            self.conn.connect((host, port))
            self.sock = self.conn
            self.peer = host
            # Set status to connected
            self.CONNECTED = True
        else:
            print "Already connected to peer", self.peer
    
    def wait_for_connect(self, port):
        """ Wait for a connection, and accept it. """
        
        if self.CONNECTED == False:
            hostname = 'localhost'
            self.conn.bind((hostname, port))
            self.conn.listen(1)
            s, addr = self.conn.accept()
            self.sock = s
            # Set status to connected
            self.CONNECTED = True
        else:
            print "Already connected to peer", self.peer
    
    def send(self, msg):
        """ Send the message (class message) given as input to connected peer. """
        
        if self.CONNECTED == False:
            print "Not connected to any peer!"
            return
        
        buf = ""
        for i in range(msg.size()):
            buf += msg.get(i) + " "
        
        # Send the length of the message
        l = str(len(buf))
        ll = str(len(l))
        self.sock.send(ll)
        self.sock.send(l)
        # Send the message
        self.sock.send(buf)
    
    def recv(self):
        """ Recieve a message (class message) from a connected peer. """
        
        if self.CONNECTED == False:
            print "Not connected to any peer!"
            return
        
        self.sock.setblocking(1)
        
        # Recieve message
        # recv wont block for some reason.... spinlocking ftw! ^^
        # Need to look in to this...
        buf = ''
        while buf == '':
            buf = self.sock.recv(1)
        ll = int(buf)
        
        buf = ''
        while buf == '':
            buf = self.sock.recv(ll)
        l = int(buf)
        
        buf = ''
        while buf == '':
            buf = self.sock.recv(l)
        
        message_list = buf.split()
        msg = message()
        
        for token in message_list:
            msg.add(token)

        return msg
        
    def cleanup(self):
        """ Close sockets and set status to not connected. """
        self.sock.close()
        self.conn.close()
        self.CONNECTED = False
    