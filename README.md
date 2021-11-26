Este repositorio contiene ejemplos de código, ya sea en forma de fragmentos o módulos completos, para que un usuario que se inicia en el desarrollo de complementos disponga de recursos que le permitan resolver con rapidez tareas concretas, siempre apoyándose en la biblioteca estándar de Python y los módulos incorporados en NVDA.

## Estructura

La estructura del repositorio recuerda a la que se podría encontrar en cualquier complemento, en el directorio scratchpad de NVDA, o en carpetas de configuración de versiones antiguas:

* appModules: contiene módulos completos que sirven como ejemplo para crear módulos de aplicación.
* globalPlugins: módulos que podrían emplearse como extensiones globales.
* brailleDisplayDrivers: módulos empleados en la construcción de controladores para pantallas Braille.
* synthDrivers: módulos utilizados para crear sintetizadores de voz.
* visionEnhancementProviders: módulos usados para construir proveedores de mejoras de la visión.
* Fragmentos: fragmentos de código independientes, que por sí solos no constituyen módulos completos, pero que podrían emplearse en cualquier parte.

## Archivos de ejemplo

Por lo general, los archivos de ejemplo tienen la extensión .py, y se encuentran dentro de las carpetas anteriores. Ten en cuenta que, a causa de caracteres acentuados, codificación de texto incorrecta u otros factores, como los comentarios, los archivos pueden no funcionar por sí mismos al emplearse en NVDA o el propio intérprete Python. Su objetivo es servir como base para aprender a programar, no como código directamente listo para utilizar.

Cada archivo contiene, en su parte superior, un comentario con el nombre del autor, el título del ejemplo y una breve descripción del mismo. A continuación comienza el código, que incluye tantos comentarios como el autor desee incorporar para que los usuarios entiendan el funcionamiento de una o varias instrucciones.

Los nombres de los archivos describen brevemente su propósito, están en minúscula y no llevan espacios. Por ejemplo: editar-modulo-aplicacion-activa.py. De esa forma, será más sencillo encontrar lo que estamos buscando.

Si un ejemplo es demasiado complejo, el autor puede colocarlo dentro de una subcarpeta en una de las carpetas anteriores, y añadir un documento extra con información, así como los módulos Python adicionales que desee.

Esperamos que este repositorio te sirva para aprender y que te animes a colaborar. ¡No dudes en abrir incidencias o pull requests para aportar sugerencias y comentarios!