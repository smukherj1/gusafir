import webapp2
from utils import *
from device import DeviceInterface
import json
import sys
from paste import httpserver
from socket import error as SocketError

_global_Device = DeviceInterface()

class NodePage(Handler):
    def get(self):
        if not _global_Device.loaded():
            print 'Device not yet loaded!'
            return self.redirect('/')

        gid = str(self.request.get('gid')).strip()
        if gid and gid.isdigit():
            node = _global_Device.getNode(int(gid))
            return self.render('show.html', node=node,
                num_fanins=len(node.fanins()),
                num_fanouts=len(node.fanouts()))

        elem = str(self.request.get('elem')).strip()
        x = str(self.request.get('x'))
        y = str(self.request.get('y'))
        z = str(self.request.get('z'))
        i = str(self.request.get('i'))

        if elem and x and x.isdigit() \
            and y and y.isdigit() \
            and z and z.isdigit() \
            and i and i.isdigit():
            node = _global_Device.lookup(elem,
                int(x),
                int(y),
                int(z),
                int(i))
            return self.render('show.html', node=node,
                num_fanins=len(node.fanins()),
                num_fanouts=len(node.fanouts()))

        return self.redirect('/')

class MainPage(Handler):
    def renderDeviceLoader(self):
        pdevice_map = _global_Device.getDeviceMap()
        pdevice_map_str = json.dumps(pdevice_map)
        return self.render('device.html', 
            device_map = pdevice_map,
            device_map_str = pdevice_map_str)

    def renderNewNode(self):
        return self.render('node.html',
            elem_list = _global_Device.getElems())

    def get(self):
        if not _global_Device.loaded():
            return self.renderDeviceLoader()
        else:
            return self.renderNewNode()

    def post(self):
        part = str(self.request.get('part')).strip()
        if part:
            print 'Loading part', part
            _global_Device.load(part)
        return self.redirect('/')

class TestPage(Handler):
    def get(self):
        return self.response.write('OK')

def main():
    host = sys.argv[1]
    port = sys.argv[2]
    testpage = sys.argv[3]

    app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/show', NodePage),
    ('/%s'%testpage, TestPage)
        ], debug=True)
    try:
        httpserver.serve(app, host=sys.argv[1], port=sys.argv[2])
    except SocketError:
        print 'Error: Failed to start webserver at http://%s:%s'%(sys.argv[1], sys.argv[2])
        exit(-1)

if __name__ == '__main__':
    main()