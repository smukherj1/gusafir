import webapp2
from utils import *
from device import DeviceInterface
import json
import sys
from paste import httpserver
from paste.urlparser import StaticURLParser
from paste.cascade import Cascade
from socket import error as SocketError
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
_global_Device = DeviceInterface()

class ElemsList(Handler):
    def get(self):
        if not _global_Device.loaded():
            return self.response.write('[]')
        elem = str(self.request.get('elem')).strip()
        if not elem:
            return self.response.write('[]')
        result = json.dumps(_global_Device.getLocs(elem))
        return self.response.write(result)

class NodePage(Handler):
    def get(self):
        if not _global_Device.loaded():
            print 'Device not yet loaded!'
            return self.response.write('The Device is still loading! Please refresh after a minute or two.')

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
            if node:
                return self.render('show.html', node=node,
                    num_fanins=len(node.fanins()),
                    num_fanouts=len(node.fanouts()))

        return self.render('node.html', error_header='Could not find that node',
            elem_list = _global_Device.getElems())

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
            print 'Info: Loading part', part
            _global_Device.load(part)
            print 'Info: Device loading complete.'
        return self.redirect('/')


def main():
    host = sys.argv[1]
    port = sys.argv[2]

    web_app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/show', NodePage),
    ('/elems', ElemsList)
        ], debug=True)
    static_app = StaticURLParser((os.path.join(SCRIPT_DIR, "static")))

    # Create a cascade that looks for static files first, then tries the webapp
    app = Cascade([static_app, web_app])
    try:
        httpserver.serve(app, host=host, port=port)
    except SocketError:
        print 'Error: Failed to start webserver at http://%s:%s'%(sys.argv[1], sys.argv[2])
        exit(-1)

if __name__ == '__main__':
    main()