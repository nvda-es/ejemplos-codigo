# -*- coding: UTF-8 -*-

# Ejemplo de una tarea de instalación que muestra las novedades de un complemento cuando se actualiza.
# (C) 2023 Javi Dominguez https://github.com/javidominguez/
# License GPL2 https://www.gnu.org/licenses/old-licenses/gpl-2.0.html#SEC1

def onInstall() -> None:
	try:
		displayChangelog("poner aquí el nombre del complemento")
	except Exception as inst:
		# Si se produce un error, se advierte en el registro pero no se lanza para evitar interrumpir la instalación.
		from logHandler import log
		log.warning(_("Fail in displayChangelog function on install tasks\n{}").format(
			"\n".join(inst.args)
		))

def displayChangelog(addonName):
	"""Muestra el registro de cambios cuando se actualiza un complemento que ya está instalado.

Cuando se instala una actualización, antes de reiniciar, en addonHandler.getAvailableAddons
Hay dos addons con el mismo nombre, el primero es el que está instalado y el otro el que está pendiente de instalar.

En la carpeta de documentación del complemento debe haber un archivo con el nombre changelog.txt

El registro de cambios se muestra si se cumplen estas condiciones:
* Se está actualizando un complemento existente, no instalando uno nuevo,
* el complemento instalado y el que se va a instalar son versiones diferentes,
* El archivo changelog.txt existe.
"""

	import addonHandler
	addonHandler.initTranslation()
	addons = filter(lambda a: a.name == addonName, addonHandler.getAvailableAddons())
	addon = next(addons)
	# Si se actualiza una versión instalada, se muestra el registro de cambios.
	if addon.isInstalled:
		fromVersion = addon.version
		addon = next(addons) # Ahora addon es el nuevo que está pendiente de ser instalado al reiniciar.
		if fromVersion == addon.version: return # Si son la misma versión salimos sin mostrar nada.
		import os
		# Buscamos el archivo changelog.txt en la carpeta de documentación.
		path = os.path.join(
			os.path.split(
			addon.getDocFilePath())[0],
			"changelog.txt")
		if not os.path.exists(path): return #Si no existe el archivo no continuamos.
		title = _("Whats new in {addonSummary} {addonVersion}").format(
			addonSummary = addon.manifest["summary"],
			addonVersion = addon.version
		)
		with open(path, "r") as f:
			body = f.read()
		import gui
		gui.messageBox(body, title)