
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
		assert(not self.__loaded)
		self.__loaded = True
		self.__part = part
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