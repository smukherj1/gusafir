import webbrowser
import subprocess
import time
import os
import urllib2
import atexit


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SERVER_SCRIPT = os.path.join(SCRIPT_DIR, 'gusafir_server.py')
HOST = '0.0.0.0'
PORT = 8080

if __name__ == '__main__':
    print 'Info: Welcome to Gusafir 2.0'
    print 'Info: Attemping to start the Gusafir Server. We will attempt 10 different ports before giving up.'
    p = None

    def cleanup():
        if p:
            try:
                p.kill()
            except OSError:
                pass
        return

    atexit.register(cleanup)
    success = False
    for iport in range(PORT, PORT + 1001, 100):
        addr = 'http://%s:%d'%(HOST, iport)
        print 'Info: Attemping to start the Gusafir Server on %s'%addr
        p = subprocess.Popen(['python' , SERVER_SCRIPT, HOST, str(iport)])
        while p.poll() == None:
            time.sleep(1)
            try:
                resp = urllib2.urlopen(addr)
                success = True
                print 'Info: Gusafir is alive at %s'%addr
                webbrowser.open(addr, autoraise=True)
                break
            except urllib2.URLError:
                pass
        if success:
            break
        else:
            try:
                p.kill()
            except OSError:
                pass
    if not success:
        print 'Error: Gusafir 2.0 failed to start :('
        exit(-1)
    elif p:
        try:
            p.wait()
        except OSError:
            pass
