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
import urllib
import logging

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
_global_Device = DeviceInterface()
_log = logging.getLogger(__name__)
logging.basicConfig(format='[%(asctime)s][%(levelname)s]   %(message)s', level=logging.INFO)
TEST_PAGE = 'test'

class ElemsList(Handler):
    def get(self):
        _log.info('GET /elems?elem=%s'%self.request.get('elem'))
        if not _global_Device.loaded():
            return self.response.write('[]')
        elem = str(self.request.get('elem')).strip()
        if not elem:
            return self.response.write('[]')
        result = json.dumps(_global_Device.getLocs(elem))
        return self.response.write(result)

class NodePage(Handler):
    def get(self):
        _log.info('GET /show?gid=%s&elem=%s&x=%s&y=%s&z=%s&i=%s'%(self.request.get('gid'),
            self.request.get('elem'),
            self.request.get('x'),
            self.request.get('y'),
            self.request.get('z'),
            self.request.get('i')))
        if not _global_Device.loaded():
            _log.warning('New Node page requested but device not yet loaded!')
            return self.redirect('/')

        gid = str(self.request.get('gid')).strip()
        if gid and gid.isdigit():
            node = _global_Device.getNode(int(gid))
            return self.render('show.html',
                part=_global_Device.part(),
                node=node,
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
                return self.render('show.html',
                    part=_global_Device.part(),
                    node=node,
                    num_fanins=len(node.fanins()),
                    num_fanouts=len(node.fanouts()))

        error = urllib.urlencode({'error' : 'Could not find that node!'})
        return self.redirect('/?' + error)

class MainPage(Handler):
    def renderDeviceLoader(self):
        pdevice_map = _global_Device.getDeviceMap()
        pdevice_map_str = json.dumps(pdevice_map)
        return self.render('device.html',
            device_map = pdevice_map,
            device_map_str = pdevice_map_str)

    def renderNewNode(self):
        error_header = self.request.get('error')
        return self.render('node.html',
            part=_global_Device.part(),
            error_header=error_header,
            elem_list = _global_Device.getElems())

    def get(self):
        _log.info('GET /')
        if not _global_Device.loaded():
            return self.renderDeviceLoader()
        else:
            return self.renderNewNode()

    def post(self):
        _log.info('POST /')
        part = str(self.request.get('part')).strip()
        if part:
            _log.info('Loading device %s'%part)
            _global_Device.load(part)
            _log.info('Finished loading device')
        return self.redirect('/')

class TestPage(Handler):
    def get(self):
        _log.info('GET /%s'%TEST_PAGE)
        return self.response.write('OK')


def main():
    host = sys.argv[1]
    port = sys.argv[2]
    global TEST_PAGE

    if len(sys.argv) > 3:
        TEST_PAGE = sys.argv[3]

    web_app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/show', NodePage),
    ('/%s'%TEST_PAGE, TestPage),
    ('/elems', ElemsList)
        ], debug=True)
    static_app = StaticURLParser((os.path.join(SCRIPT_DIR, "static")))

    # Create a cascade that looks for static files first, then tries the webapp
    app = Cascade([static_app, web_app])
    try:
        httpserver.serve(app, host=host, port=port)
    except SocketError:
        _log.error('Failed to start webserver at http://%s:%s'%(host, port))
        exit(-1)

if __name__ == '__main__':
    main()
