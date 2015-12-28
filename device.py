from threading import Lock
_device_loader_lock = Lock()


class Node:
	def __init__(self, gid, name, rtl_name, fanins=[], fanouts=[]):
		self.__gid = gid
		self.__name = name
		self.__rtl = rtl_name
		self.__fanins = list(fanins)
		self.__fanouts = list(fanouts)

	def gid(self):
		return self.__gid

	def name(self):
		return self.__name

	def rtl(self):
		return self.__rtl

	def fanins(self):
		return self.__fanins

	def fanouts(self):
		return self.__fanouts

class DeviceInterface:
	def __init__(self):
		self.__loaded = False
		self.__part = None
		return

	def load(self, part):
		_device_loader_lock.acquire()
		try:
			if not self.__loaded:
				self.__part = part
				self.__loaded = True
		finally:
			_device_loader_lock.release()
		return

	def loaded(self):
		return self.__loaded

	def getDeviceMap(self):
		return {
			"Family 1" : ["F1Device 1", "F1Device 2"],
			"Family 2" : ["F2Device 1", "F2Device 2"],		
		}

	def getElems(self):
		return [ "ELEM1",
		"ELEM2",
		"ELEM3",
		"ELEM4"
		]

	def lookup(self, elem, x, y, z, i):
		gid = int(x) * 1000 + int(y) * 100 + int(z) * 10 + int(i)
		return self.getNode(gid)

	def getNode(self, gid):
		n = Node(gid, 'FAKE', 'fakemux:muxout', 
				[
					Node(gid + 1, 'FAKE_FANIN', 'imux:muxout'),
					Node(gid + 2, 'FAKE_FANIN', 'imux:muxout'),
					Node(gid + 3, 'FAKE_FANIN', 'imux:muxout'),
				],
				[
					Node(gid + 4, 'FAKE_FANOUT', 'omux:muxout'),
					Node(gid + 5, 'FAKE_FANOUT', 'omux:muxout'),
					Node(gid + 6, 'FAKE_FANOUT', 'omux:muxout'),
					Node(gid + 7, 'FAKE_FANOUT', 'omux:muxout')
				]
			)
		return n