# -*- coding: utf-8 -*-

class message:
	""" Class encapsulating messages.
		Used with the protocolBase for transferring messages between peers. """

	def __init__(self):
		""" Initializes the object with a message (string) if input is given. """
		self.msg = []

	def add(self, msg):
		""" Add a message to the list of messages. """
		self.msg.append(msg)

	def get(self, idx):
		""" Get the message at the given index. """
		try:
			retval = self.msg[idx]
		except:
			retval = False
			print "Index out of range"
		return retval

	def size(self):
		""" Retrieve the number of messages in this meessage. """
		return len(self.msg)
