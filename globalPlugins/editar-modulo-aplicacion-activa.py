# Autor: Javi Domínguez
# Este ejemplo permite cargar el módulo de la aplicación activa, si existe, en el editor por defecto.
# Imprescindible asociar en el sistema un editor de texto con la extensión .py
# Importación de módulos
import globalPluginHandler
import appModuleHandler
import appModules
import api
import ui
import os

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Script que abre el módulo de la aplicación activa en el editor de texto por defecto, si existe
	def script_openModuleSourcecode(self, gesture):
		fg = api.getForegroundObject()  # Obtiene el objeto asociado a la ventana activa
		try:
			file = getattr(appModules, fg.appModule.appModuleName).__file__  # Archivo del módulo de aplicación
		except AttributeError:  # si falla, no hay módulo de aplicación para el programa activo
			ui.message(_("There are not appModule for %s" % fg.appModule.productName))
		else:  # continuamos donde lo dejamos, no hubo errores
			# Si el archivo acaba en .pyo, buscamos uno equivalente acabado en .py
			if file[-4:].lower() == ".pyo":
				file = file[:-1]
			if os.path.exists(file):
				# Y si existe, lo abrimos con el programa asociado, que debería ser un editor de texto
				os.startfile(file)
			else:  # Si no existe, lo comunicamos al usuario con un mensaje hablado y por Braille
				ui.message(_("Sourcecode of %s appModule is not available.") % fg.appModule.appModuleName)

	__gestures = {  # Diccionario de gestos
	"kb:NVDA+Control+Shift+F1": "openModuleSourcecode"
	}
	