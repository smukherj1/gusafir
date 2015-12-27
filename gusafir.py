import webapp2
from utils import *
from device import DeviceInterface
import json

_global_Device = DeviceInterface()

class NodePage(Handler):
    def get(self):
        return self.response.write('Showing node!')

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