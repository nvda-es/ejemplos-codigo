# Ejemplo de creacion de menus virtuales, sin interfaz grafica, en NVDA
# This file is covered by the GNU General Public License.
# Copyright (C) Javi Dominguez 2021

import globalPluginHandler
from keyboardHandler import KeyboardInputGesture
from string import ascii_uppercase
from functools import wraps
import tones
import ui

# El codigo a continuacion no es mio, es originalmente de Tyler Spivey con mejoras de Joseph Lee.
# Es necesario ponerlo aqui para que luego la capa de teclado funcione bien
def finally_(func, final):
	"""Calls final after func, even if it fails."""
	def wrap(f):
		@wraps(f)
		def new(*args, **kwargs):
			try:
				func(*args, **kwargs)
			finally:
				final()
		return new
	return wrap(final)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)

		""" Almacenamos el menu en alguna estructura de variables.
		A mi me gustan los diccionarios, son mas compactos y claros a la hora de referenciar su contenido,
		pero para este ejemplo voy a usar tuplas y listas para que se vea mejor lo que estoy haciendo. """

		# Una lista para las categorias (uso una lista porque una tupla daria error en script_skipToCategory):
		self.categorias = ["Categoria 1", "Categoria 2", "Categoria 3"]
		# Una matriz para los items de cada categoria. Cada fila es una categoria.
		self.items = (
		# Categoria 1:
		("Item 1", "Item 2", "Item 3"),
		# Categoria 2:
		("Item 4", "Item 5", "Item 6"),
		# Categoria 3:
		("Item 7", "Item 8", "Item 9")
		)

		""" Ahora se puede abordar el tema de dos maneras.
		Una seria usando condicionales. Si indices == (1, 2) entonces hacer la accion correspondiente a "Item 6" y asi con todos.
		Pero a mi me gusta mas usar funciones y para eso necesito otra matriz.
		Voy a usar una unica funcion para aligerar pero en un caso real hay que tener cuidado de poner cada una en la posicion correspondiente a la matriz de items. """

		def holaMundo():
			ui.message("Hola, mundo")

		self.acciones = (
		# Categoria 1:
		(holaMundo, holaMundo, holaMundo), # Sin comillas, eh? Hace referencia a la funcion.
		# Categoria 2:
		(holaMundo, holaMundo, holaMundo),
		# Categoria 3: (aqui voy a variar un poco para que no sea tan repetitivo)
		(lambda: ui.message("Hola, mundo"), lambda: ui.message("Hola, mundo"), lambda: ui.message("Hola, mundo"))
		)
		
		# por ultimo un par de indices:
		self.catIndex = 0
		self.itemIndex = 0

		# Aqui guardaremos los enlaces a los gestos originales para restaurarlos despues
		self.oldGestureBindings = {}
		# Este flag nos indica si la capa de teclado esta activa o no
		self.toggling = False
		# Este otro flag indica si es la primera vez que se lanza el menu.
		self.firstTime = True
		# y con esto tenemos el menu construuido, nos falta darle vida.

	def getScript(self, gesture):
		""" Esta funcion es la encargada de lanzar los scripts. Es un metodo de la clase GlobalPlugin que vamos a tunear.
		Recibe un gesto y devuelve el script asociado a el, que sera ejecutado.
		Vamos a modificarlo para que lance el scrip que a nosotros nos interese. """
		if not self.toggling:
			# Si la capa de teclado no esta activa devuelve el script "normal" asociado a gesture.
			return globalPluginHandler.GlobalPlugin.getScript(self, gesture)
		""" Si la capa de teclado, es decir, el menu, esta activo, seguimos.
		metemos en la variable script el script asociado a gesture.
		Parece lo mismo de antes pero no lo es, ya que al activar la capa de teclado habremos eliminado las asociaciones originales y las habremos sustituido por las que nos interese. """ 
		script = globalPluginHandler.GlobalPlugin.getScript(self, gesture)
		if not script:
			if "kb:escape" in gesture.identifiers:
				# Si el gesto no tiene ningun script asociado, comprobamos si la tecla pulsada ha sido escape y en ese caso sale, para ello metemos en la variable script a finally_, la funcion que pusimos al principio y  que envuelve a script_exit y a finish.
				script = finally_(self.script_exit, self.finish)
			else:
				""" Si ha sido cualquier otra tecla, metemos en finally_ el script de ayuda y una funcion lambda vacia.
				La funcion lambda es necesaria porque a finally_ hay que pasarle una funcion pero en este caso tiene que ser una que no haga nada para que el menu siga activo.
				Si en lugar de un menu quisieramos hacer una capa de ordenes de dos pulsaciones, como en Instant translate, en lugar de una funcion vacia aqui pondriamos finish. """
				script = finally_(self.script_speechHelp, lambda: None) 
		return script
		""" Esto es un tema de funciones envueltas que no es cuestion de explicar aqui.
		Resumiendo: finally_ ejecutara la funcion finish precedida de un mensaje de salida (script_exit) o del script asociado al gesto, segun el caso. """ 

	def script_exit(self, gesture):
		""" Este script se ejecuta cuando salimos del menu.
		Se ejecutara antes de finish y ambas envueltas por finally_ """ 
		ui.message("Saliendo del menu")

# y aqui tenemos a la famosa finish con lo que todo terminara.
	def finish(self):
		""" Pone el flag a false para indicar que la capa de teclado esta inactiva,
		borra todas las asociaciones de gestos
		y restituye los originales. """
		self.toggling = False
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)
		# Con esto nos aseguramos de devolverle el control de sus gestos a otros modulos, plugins o a quien se los hayamos quitado antes:
		for key in self.oldGestureBindings:
			script = self.oldGestureBindings[key]
			if hasattr(script.__self__, script.__name__):
				script.__self__.bindGesture(key, script.__name__[7:])

# Y aqui el script con lo que todo empezara:
	def script_activarMenu(self, gesture):
		""" Esta funcion es la que activara el menu. """
		if self.toggling:
			# Si ya estaba activado, sale.
			self.script_exit(gesture)
			self.finish()
			return
		for k in ("upArrow", "downArrow", "leftArrow", "rightArrow", "enter", "shift+enter", "control+enter", "numpadEnter", "shift+numpadEnter", "control+numpadEnter", "escape", "backspace", "F1", "F12", "numpad2", "numpad4", "numpad5", "numpad6", "numpad8", "numpadPlus", "numpadMinus", "numpadDelete"):
			""" Guardamos los scripts asociados a las teclas que vamos a usar para devolverselos a sus propietarios mas tarde, cuando salgamos del menu.
			Tambien borraremos los enlaces antes de asignar los nuevos, para evitar conflictos de teclado. """
			try:
				script = KeyboardInputGesture.fromName(k).script
			except KeyError:
				script = None
			if script and self != script.__self__:
				try:
					script.__self__.removeGestureBinding("kb:"+k)
				except KeyError:
					pass
				else:
					self.oldGestureBindings["kb:"+k] = script
		self.bindGestures(self.__menuGestures) # Enlazamos el nuevo juego de gestos a sus correspondientes scripts
		for c in ascii_uppercase:
			# Enlazamos caracteres individuales al script skipToCategory para saltar a la categoria por la letra inicial. (Esto solo funciona en distribuciones de teclado occidentales con alfabetos latinos).
			self.bindGesture("kb:"+c, "skipToCategory")
		# Por ultimo, ponemos el flag a True para indicar que el menu esta activo.
		self.toggling = True
		# y anunciamos un mensaje
		ui.message("Menu activado")
		if self.firstTime:
			# Cuando se ejecuta por primera vez anunciamos la ayuda. (opcional)
			self.script_speechHelp(None)
			self.firstTime = False

# Este diccionario contiene los gestos normales, los que estaran enlazados cuando el menu este inactivo. Suele ir al final pero lo pongo aqui para que quede mas claro.
	__gestures = {
	"kb:NVDA+escape": "activarMenu"
	}

	# Este otro diccionario contiene los gestos que se enlazaran cuando el menu se active.
	__menuGestures = {
	"kb:rightArrow": "nextCategory",
	"kb:leftArrow": "previousCategory",
	"kb:downArrow": "nextItem",
	"kb:upArrow": "previousCommand",
	"kb:enter": "executeCommand",
	"kb:numpadEnter": "executeCommand",
	}

	""" Los scripts que vienen a continuacionsolo se podran invocar cuando el menu este activo y por lo tanto se hallan enlazado a los gestos de __menuGestures.
	Estos scripts son los que moveran el menu y ejecutaran el comando correspondiente cuando se pulse enter """

	def script_nextCategory(self, gesture):
		self.catIndex = self.catIndex+1 if self.catIndex < len(self.categorias)-1 else 0
		ui.message(self.categorias[self.catIndex])
		self.itemIndex = -1

	def script_previousCategory(self, gesture):
		self.catIndex = self.catIndex -1 if self.catIndex > 0 else len(self.categorias)-1
		ui.message(self.categorias[self.catIndex])
		self.itemIndex = -1

	def script_skipToCategory(self, gesture):
		categories = (self.categorias[self.catIndex+1:] if self.catIndex+1 < len(self.categorias) else []) + (self.categorias[:self.catIndex])
		try:
			self.catIndex = self.categorias.index(filter(lambda i: i[0].lower() == gesture.mainKeyName, categories).__next__())-1
		# Compatibility with Python 2
		except AttributeError:
			try:
				self.catIndex = self.categorias.index(filter(lambda i: i[0].lower() == gesture.mainKeyName, categories)[0])-1
				self.script_nextCategory(None)
			except IndexError:
				if self.categorias[self.catIndex][0].lower() == gesture.mainKeyName:
					ui.message(self.categorias[self.catIndex])
				else:
					tones.beep(200, 30)
		# End of compatibility with Python 2
		except StopIteration:
			if self.categorias[self.catIndex][0].lower() == gesture.mainKeyName:
				ui.message(self.categorias[self.catIndex])
			else:
				tones.beep(200, 30)
		else:
			self.script_nextCategory(None)

	def script_nextItem(self, gesture):
		self.itemIndex = self.itemIndex + 1 if self.itemIndex < len(self.items)-1 else 0
		ui.message(self.items[self.catIndex][self.itemIndex])

	def script_previousCommand(self, gesture):
		self.itemIndex = self.itemIndex-1 if self.itemIndex > 0 else len(self.items)-1
		ui.message(self.items[self.catIndex][self.itemIndex])

	def script_executeCommand(self, gesture):
		if self.itemIndex < 0:
			ui.message("use flechas derecha e izquierda para moverse por las categorias, flehchas arriba y abajo para seleccionar item, enter para activarlo o escape para salir.")
			return
		""" Aqui es donde se ejecuta la accion asociada al item que se ha seleccionado.
		Dependiendo de lo que quieras hacer puede ser mas o menos complicado.
		En este ejemplo simplemente llamaremos a la funcion correspondiente de las que almacenamos en la matriz de acciones. """
		self.acciones[self.catIndex][self.itemIndex]()

	def script_speechHelp(self, gesture):
		ui.message("use flechas derecha e izquierda para moverse por las categorias, flehchas arriba y abajo para seleccionar item, enter para activarlo o escape para salir.")

