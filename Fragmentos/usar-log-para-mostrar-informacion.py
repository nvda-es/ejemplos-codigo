# Autor: José Manuel Delicado
# Este fragmento muestra cómo usar el registro de NVDA para grabar información y clasificarla según su importancia
# Normalmente, en Python disponemos de la función print para emitir mensajes por consola
# Sin embargo, aunque en NVDA print genera un mensaje en el registro, no es la alternativa más adecuada
# Para usar el registro, necesitamos un objeto de un módulo
from logHandler import log
# ahora, llamamos a una de las siguientes funciones, según el mensaje que queramos transmitir
# El mensaje sólo se verá en el registro si se ha configurado el nivel de registro adecuado en las opciones generales de NVDA
# Nivel información
log.info("Este es un mensaje informativo.")
log.warning("Este es un mensaje de aviso que indica que algo no va bien, pero que podemos recuperarnos y continuar. Al llamar a print, se genera uno de estos")
log.error("Este es un mensaje de error")
log.critical("Este es un mensaje de error crítico. NVDA emitirá un sonido de error mientras lo graba en el registro")
# Nivel aviso de depuración
log.debugWarning("Este es un mensaje de aviso de depuración. Algo no ha ido como se esperaba, pero no es tan grave como para que afecte al usuario.")
# Nivel entrada / salida
log.io("Este es un mensaje de entrada / salida. Aquí registramos interacciones con red, periféricos del equipo y síntesis de voz, por ejemplo.")
# Nivel depuración
log.debug("Este es un mensaje de depuración. Útil para que un desarrollador pueda saber si su complemento hace lo que se espera en el momento adecuado")
