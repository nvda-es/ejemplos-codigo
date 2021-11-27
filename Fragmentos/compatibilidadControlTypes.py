# -*- coding: UTF-8 -*-

""" compatibilidad del módulo controlTypes con versiones antiguas de NVDA

Javi Doninguez (Nov 2021) 

El módulo controlTypes almacena los valores para los roles de los objetos, sus estados y sus etiquetas.
En versiones antiguas se referenciaban estos valores directamente en el espacio de nombres de controlTypes, por ejemplo, así:

controlTypes.ROLE_window
controlTypes.STATE_SELECTED

A partir de la versión 2019.3 este módulo se reorganizó cambiando los nombres de las variables e incluyéndolas en submódulos y objetos enumeradores de modo que ha cambiado la manera de referenciarlas. Ahora seríam por ejemplo:

controlTypes.Role.WINDOW
controlTypes.State.SELECTED

Por compatibilidad se mantuvieron las variables antiguas de forma que podían referenciarse de ambas maneras pero a partir de la próxima versión 2022.1 se eliminarán y sólo será válida la nueva.
Todos los complementos que usen controlTypes tendrán que actualizarse para cambiar las referencias a roles, states, etc.

El problema entonces es que esos complementos dejarán de funcionar en las versiones anteriores de NVDA.
El código a continuación soluciona este problema.
Está inspirado en el compartido por Alberto Buffolino en la lista de correo de complementos
https://nvda-addons.groups.io/g/nvda-addons/message/17328

Está probado en la última Versión alpha-24281,3de944cf disponible de NVDA a fecha de hoy. Si hubieran cambios posteriores habría que adaptarlo.
"""

import controlTypes
# controlTypes module compatibility with old versions of NVDA
if not hasattr(controlTypes, "Role"):
	setattr(controlTypes, "Role", type('Enum', (), dict(
	[(x.split("ROLE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("ROLE_")])))
	setattr(controlTypes, "State", type('Enum', (), dict(
	[(x.split("STATE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("STATE_")])))
	setattr(controlTypes, "role", type("role", (), {"_roleLabels": controlTypes.roleLabels}))
# End of compatibility fixes

"""Explicación

Arriba está expresado de forma compacta, voy a hacerlo desglosado para que se entienda mejor:

# Si controlTypes no contiene el atributo Role es que se ha importado la versión antigua 
roles = [] # inicializamos una lista vacía. 
for x in dir(controlTypes): # Recorremos todos los atributos de controlTypes 
    if x.startswith("ROLE_"): # Si el nombre del atributo empieza por ROLE_ 
        clave = x.split("ROLE_")[1] # Guardamos el nombre del atributo quitándole "ROLE_" del principio 
        valor = getattr(controlTypes, x) # Guardamos el valor del atributo 
        roles.append((clave, valor)) # Añadimos a una lista el par clave,valor. 
# Ya tenemos una lista con los nombre/valor de los atributos que corresponden a las constantes ROLE_XXX. Ahora convertimos la lista en un diccionario: 
dictRoles = dict(roles) 
# Ahora creamos un objeto de clase enum (enumerador) a partir de esa lista 
# Para ello usamos type que recibe como parámetros el nombre de la nueva clase, una tubpla vacía (no sé por qué exactamente) y un diccionario. 
objetoRole = type('Enum', (), dictRoles) 
# Por último añadimos ese objeto a controlTypes 
setattr(controlTypes, "Role", objetoRole) 
# Lo mismo habría que hacer con State y roleLabels 
"""
