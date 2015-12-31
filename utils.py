import webapp2
import jinja2
import os
import logging
import datetime
from colorama import Fore, Back, Style
from colorama import init as colorama_init

# Configure Jinja
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir),
	autoescape= True)

# Configure colorama
colorama_init(autoreset=True)

# Configure the logger
#logging.basicConfig(format='[%(asctime)s][%(levelname)s]   %(message)s', level=logging.INFO)
logging.basicConfig(format='%(message)s', level=logging.INFO)

class CLogger:
	def __init__(self, name):
		self.__logger = logging.getLogger(name)

	@classmethod
	def timestr(cln):
		msg = '[' + datetime.datetime.today().strftime('%a %b %d %I:%M:%S %p') + ']'
		return msg

	def debug(self, msg, *args, **kwargs):
		msg = 'Debug: ' + self.timestr() + ' ' + msg
		return self.__logger.debug(msg, *args, **kwargs)

	def info(self, msg, *args, **kwargs):
		msg = Fore.GREEN + Style.BRIGHT + 'Info: ' + self.timestr() + ' ' + msg
		return  self.__logger.info(msg, *args, **kwargs)

	def warning(self, msg, *args, **kwargs):
		msg = Fore.CYAN + Style.BRIGHT + 'Warning: ' + self.timestr() + ' ' + msg
		return  self.__logger.warning(msg, *args, **kwargs)

	def critical(self, msg, *args, **kwargs):
		msg = Fore.YELLOW + Style.BRIGHT + 'Critical Warning: ' + self.timestr() + ' ' + msg
		return  self.__logger.critical(msg, *args, **kwargs)

	def error(self, msg, *args, **kwargs):
		msg = Fore.RED + Style.BRIGHT + 'Error: ' + self.timestr() + ' ' + msg
		return  self.__logger.error(msg, *args, **kwargs)

class Handler(webapp2.RequestHandler):
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		acds_dest_root = str(os.environ.get('ACDS_DEST_ROOT'))
		self.response.write(self.render_str(template,
				acds_dest_root=acds_dest_root,
				**kw))
