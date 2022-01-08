# Autor: José Manuel Delicado
# Este ejemplo muestra cómo implementar el inicio retardado de tareas de red
# A priori, asumimos que todas las conexiones a Internet son directas y no necesitaremos esta funcionalidad
# Sin embargo, si es necesario aplicar un parche en las funciones de red (por ejemplo, al usar un servidor proxy), el plugin no se inicia correctamente, ya que no puede aprovechar el parche

# Importamos los módulos necesarios
import core
from threading import Thread
import globalPluginHandler
from urllib import request
from logHandler import log
import globalVars

# Clase principal
class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	# Constructor
	def __init__(self):
		# Comprobaciones de seguridad
		if globalVars.appArgs.secure:
			return
		# Llamamos al constructor de la clase padre
		super(GlobalPlugin, self).__init__()
		# Inicializamos algunas variables
		self.var = "value"
		# Registramos un manejador en el punto de extensión core.postNvdaStartup
		# Este manejador llamará al hilo encargado de realizar operaciones de red
		core.postNvdaStartup.register(self.postStartupHandler)
		# self.postStartupHandler sólo se ejecutará una vez. Por tanto, no funcionará al recargar plugins con NVDA+control+f3
		# Para solucionar este problema, podemos almacenar una variable auxiliar en globalVars, y llamar manualmente a la función sólo si la variable existe
		if hasattr(globalVars, 'miComplemento'):
			self.postStartupHandler()
		globalVars.miComplemento = None

	def postStartupHandler(self):
		# Creamos un hilo para ejecutar tareas de red de forma concurrente
		hilo = Thread(target=self.tareasDeRed)
		hilo.daemon = True
		hilo.start()

	def tareasDeRed(self):
		# Esta función se conecta a la web nvda.es y graba en el registro el resultado de la operación
		try:
			req = request.urlopen("https://nvaccess.org")
			req.close()
			log.info("Me he conectado a la web de NV Access")
		except:
			log.error("Algo ha salido mal")

	# Finalmente, liberamos recursos
	def terminate(self):
		core.postNvdaStartup.unregister(self.postStartupHandler)
