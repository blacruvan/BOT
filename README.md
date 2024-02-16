BOT de Telegram con menú de botones

Funciones:
  1. Weather: muestra el tiempo de la región seleccionada.
  2. NASA: muestra la Astronomy Picture of the Day y su descripción.
  3. Jokes: genera un chiste aleatorio.
  4. Convert: hace la conversión de csv a json y viceversa.
  5. Stats: muestra la información y estadística de un csv.
  6. Newsletter: muestra las noticias en la portada de eldiario.com
  7. Cinema: muestra la cartelera del cine seleccionado.
  8. Trivia: preguntas interaactivas de trivial.
  9. Ocio: muestra actividades próximas en el lugar seleccionado.
  10. Inferno: accede a la BD y devuelve la información.

Instrucciones:
  1. Descargar la imagen del docker con el comando:
       > docker push vaneebc/bot:latest
  2. Lanzar el docker usando el TOKEN como parámetro:
       > docker run --rm -e TOKEN=xxx vaneebc/bot:latest
  3. Buscar el bot en Telegram con el nombre de:
       > @vanee_bot


LISTO!!
