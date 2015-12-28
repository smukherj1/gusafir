import webapp2
from utils import *
from device import DeviceInterface
import json

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


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/show', NodePage)
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='0.0.0.0', port='8080')

if __name__ == '__main__':
    main()