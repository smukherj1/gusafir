import json

ROWS = 100
COLS = 100


_global_Nodes = []
_global_coord_idx_map = {}
NODE_TYPES = ["CLOCK", "LAB", "HWIRE", "VWIRE", "IO"]

def genNodes(rows, cols):
	for ir in range(rows):
		_global_coord_idx_map[ir] = {}
		for ic in range(cols):
			_global_coord_idx_map[ir][ic] = {}
			for itype in NODE_TYPES:
				node = {}
				node["gid"] = len(_global_Nodes)
				node["name"] = "%s_X%dY%dZ0I0"%(itype, ic, ir)
				node["rtl_name"] = "%s_r%d_c%d:muxout"%(itype.lower(), ir, ic)
				node["fanins"] = []
				node["fanouts"] = []
				_global_coord_idx_map[ir][ic][itype] = len(_global_Nodes)
				_global_Nodes.append(node)

	return

def genConnectivity(rows, cols):
	idx = -1
	for ir in range(rows):
		for ic in range(cols):
			for itype in NODE_TYPES:
				idx += 1
				if ir > 0:
					_global_Nodes[idx]["fanouts"].append(_global_coord_idx_map[ir - 1][ic][itype])
				if ir < (rows - 1):
					_global_Nodes[idx]["fanouts"].append(_global_coord_idx_map[ir + 1][ic][itype])
				if ic > 0:
					_global_Nodes[idx]["fanouts"].append(_global_coord_idx_map[ir][ic - 1][itype])
				if ic < (cols - 1):
					_global_Nodes[idx]["fanouts"].append(_global_coord_idx_map[ir][ic + 1][itype])
				_global_Nodes[idx]["fanins"] = _global_Nodes[idx]["fanouts"]
	return

def dumpNodes():
	f_out = open('device.json', 'w')
	json.dump(_global_Nodes, f_out, indent=1)
	return

if __name__ == '__main__':
	genNodes(ROWS, COLS)
	genConnectivity(ROWS, COLS)
	dumpNodes()
