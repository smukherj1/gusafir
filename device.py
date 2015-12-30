from threading import Lock
import time
import json
import re

XYZI_RE = re.compile(r'[a-zA-Z]+_X(\d+)Y(\d+)Z(\d+)I(\d+)')
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

def parseNodeName(name):
	match = XYZI_RE.match(name)
	x = int(match.group(1))
	y = int(match.group(2))
	z = int(match.group(3))
	i = int(match.group(4))
	return x, y, z, i

class DeviceInterface:
	def __init__(self):
		self.__loaded = False
		self.__part = None
		self.__nodes = []
		return

	def __load(self):
		f_in = open('device.json')
		nodes = json.load(f_in)
		for iraw_node in nodes:
			n = Node(**iraw_node)
			assert(n.gid() == len(self.__nodes))
			self.__nodes.append(n)
		return

	def load(self, part):
		_device_loader_lock.acquire()
		try:
			if not self.__loaded:
				self.__part = part
				self.__load()
				self.__loaded = True
				#time.sleep(5)
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
		return ["CLOCK", "LAB", "HWIRE", "VWIRE", "IO"]

	def getLocs(self, elem):
		locs = {}
		for inode in self.__nodes:
			if not inode.name().startswith(elem.upper()):
				continue
			x, y, z, i = parseNodeName(inode.name())
			if x not in locs:
				locs[x] = {}
			if y not in locs[x]:
				locs[x][y] = {}
			if z not in locs[x][y]:
				locs[x][y][z] = []
			locs[x][y][z].append(i)
		return locs

	def lookup(self, elem, x, y, z, i):
		for inode in self.__nodes:
			ix, iy, iz, ii = parseNodeName(inode.name())
			if inode.name().startswith(elem) and ix == x and iy == y and iz == z and ii == i:
				return self.getNode(inode.gid())
		return

	def getNode(self, gid):
		if gid >= 0 and gid < len(self.__nodes):
			fanins = []
			fanouts = []
			for ifanin in self.__nodes[gid].fanins():
				fanins.append(Node(ifanin, self.__nodes[ifanin].name(), self.__nodes[ifanin].rtl()))
			for ifanout in self.__nodes[gid].fanouts():
				fanouts.append(Node(ifanout, self.__nodes[ifanout].name(), self.__nodes[ifanout].rtl()))
			node = Node(self.__nodes[gid].gid(), self.__nodes[gid].name(), self.__nodes[gid].rtl(), fanins, fanouts)
			return node
		return
