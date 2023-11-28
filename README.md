# Proyecto individual 1 Machine Learning Operations (MLOps)

![Alt text](steam_4.png)

## Introducción
En este proyecto, se pide desarrollar el rol de un ingeniero de datos y de un científico de datos, para la empresa *Steam*, la cual requiere un modelo de recomendación de videojuegos que se consume a través de una API, al igual que 5 funciones que devuelven ciertos datos requeridos por la empresa.

Se nos proveen 3 datasets para trabajar con ellos y obtener los resultados:

- **steam_games.json.gz**: contiene el id del juego, app_name es el nombre del juego, developer es el desarrollador, publisher es la empresa o empresas que lo publicaron, release_date es la fecha de lanzamiento del juego, url del juego, tags que contiene etiquetas que clasifican los juegos tanto en género como en otras clasificaciones, title es el título del juego, reviews_url tiene el link a las reviews del juego, price es el precio en dólares del juego, early_access es si el juego tiene acceso previo al lanzamiento.

- **user_reviews.json.gz**: funny es si les pareció divertido el juego, posted la fecha en que se hizo la review, last_edited cuando se editó la review por última vez, item_id es el id del juego que se está haciendo la review, helpful si a otros usuarios les parece de ayuda la review, recommend si el usuario que publicó la review recomienda el juego, review contiene la review del usuario, user_id contiene el id del usuario que publicó la review.

- **users_items.json.gz**: item_id es el id del juego, item_name es el nombre del juego, playtime_forever son los minutos acumulados que lleva el usuario para ese juego, playtime_2weeks son los minutos jugados en las últimas 2 semanas para el juego dado, user_id es el id del usuario de los datos citados previamente.

## ETL

Se realizó la limpieza de los datasets quitando las filas nulas, también las columnas que no nos servían para las funciones requeridas, se quitaron valores duplicados y a través de webscraping se trató de obtener los valores nulos faltantes en algunas partes. Se imputaron valores nulos en algunos datos, en otros se cambiaron por el valor 'N/D' para no afectar la integridad de los datos que podían ser útiles para algunas funciones. Se normalizaron las fechas a modo de solo tener el año, al igual que algunas se obtuvieron con webscraping.

Una vez limpios y transformados los datos para nuestros requerimientos, se guardaron en un CSV para uso posterior.

Con un análisis de sentimientos se evaluó si la review escrita era positiva=2, negativa=0 o neutral=1.

El ETL se realizó en un solo Jupyter notebook; para verlo de forma detallada, se encuentra aquí [ETL.ipynb](https://github.com/JUrielCerecero/PI-MLOPS/blob/main/ETL.ipynb).

## EDA

Se realizó un EDa, donde se vieron los principales descurbrimientos estadísticos sobre los datos que se nos piden en las cosignas, dándonos un panorama más amplio sobre como están organizados los datos de los datasets.
se utilizaron las librerías de seborn, maptplotlib y plotly.

# Modelo de recomendación

Se opta por usar un modelo de recomendación item-item, donde se ingresa un id de un videojuego, y basado en un modelo de similitud del coseno que busca las similitudes de los vectores, vectorizando cada palabra, en este caso los géneros. Se obtienen juegos donde hay géneros similares. Se utilizó la librería de scikit learn para usar este modelo; se usaron dummies de los géneros, ya que era más efectivo en este caso porque algunos géneros constaban con expresiones regulares y al usar dummies solo se contaban los géneros.

Una vez hecho el modelo, se extrae un top 5 con mayor similitud, y se enlistan los 5 recomendados para cada juego, se relaciona con su id y el nombre para los valores de entrada y de salida. Se trabajó este modelo en el siguiente Jupyter notebook: [modelo1](https://github.com/JUrielCerecero/PI-MLOPS/blob/main/modelo1.ipynb), y se guardaron los datos para consumirse en la API en un CSV.
+ def **recomendacion_juego(*`id de producto`*)**:
    Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

    CSV: [consulta_modelo1.csv](https://github.com/JUrielCerecero/PI-MLOPS/blob/main/consulta_modelo1.csv)

## Funciones

Se pedían 5 funciones enlistadas a continuación. Las funciones se desarrollaron primero en un Jupyter notebook mencionado a continuación: [Funciones](https://github.com/JUrielCerecero/PI-MLOPS/blob/main/Funciones.ipynb). Se hicieron archivos CSV para cada consulta de cada función citadas en la descripción de cada función.

+ def **PlayTimeGenre(*`género`: str*)**:
    Devuelve `año` con más horas jugadas para dicho género.

Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X": 2013}

CSV: [Función_PlayTimeGenre.csv](https://github.com/JUrielCerecero/PI-MLOPS/blob/main/Funci%C3%B3n_PlayTimeGenre.csv)

+ def **UserForGenre(*`género`: str*)**:
    Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

Ejemplo de retorno: {"Usuario con más horas jugadas para Género X": us213ndjss09sdf, "Horas jugadas": [{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

CSV: [Función_UserForGenre.csv](https://github.com/JUrielCerecero/PI-MLOPS/blob/main/Funci%C3%B3n_UserForGenre.csv)
+ def **UsersRecommend(*`año`: int*)**:
   Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
  
Ejemplo de retorno: [{"Puesto 1": X}, {"Puesto 2": Y}, {"Puesto 3": Z}]

CSV: [Función_UsersRecommend.csv](https://github.com/JUrielCerecero/PI-MLOPS/blob/main/Funci%C3%B3n_UsersRecommend.csv)

+ def **UsersWorstDeveloper(*`año`: int*)**:
   Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
  
Ejemplo de retorno: [{"Puesto 1": X}, {"Puesto 2": Y}, {"Puesto 3": Z}]

CSV: [Función_UsersWorstDeveloper.csv](https://github.com/JUrielCerecero/PI-MLOPS/blob/main/Funci%C3%B3n_UsersWorstDeveloper.csv)

+ def **sentiment_analysis(*`empresa desarrolladora`: str*)**:
    Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.

Ejemplo de retorno: {'Valve': [Negative = 182, Neutral = 120, Positive = 278]}

CSV: [Función_sentiment_analysis.csv](https://github.com/JUrielCerecero/PI-MLOPS/blob/main/Funci%C3%B3n_sentiment_analysis.csv)

 Una vez hechas las funciones se llevan a un archivo nombrado main.py, donde se encuentran las funciones para consumir la API. Se utiliza la librería de FastApi para hacer la API con las funciones creadas anteriormente, se prueban en un ambiente local para probar su desempeño correcto antes de ser desplegadas y poder hacer los ajustes necesarios para que puedan ser consumidas una vez desplegadas.

## Despliegue

Una vez desarrollada la API en forma local, se utiliza la plataforma de Render para hacer el despliegue y la API pueda ser consumida desde cualquier dispositivo.
Se crea un Dockerfile donde se usa la versión 3.11.6 de python, esto porque Render no cuenta con esta versión de python, pero permite usar un contenedor de docker para deployar tus proyectos [Docckerfile](https://github.com/JUrielCerecero/PI-MLOPS/blob/main/Dockerfile)
En nuestros requirements se pone las librerías que usamos para nuestra API, al usar un Dockerfile tambien nos permite usar las últimas versiones de fastapi, pandas y uvicorn, por lo que dejamos sin especificar la versión en nuestros requirements. [requirements](https://github.com/JUrielCerecero/PI-MLOPS/blob/main/requirements.txt)
Una vez que tenemos nuestro Dockerfile, y nuestros requirements se deploya todo en la plataforma de Render.
Este es un pequeño tutorial [Tutorial Render fastapi](https://github.com/HX-FNegrete/render-fastapi-tutorial) de como hacer un deploy sencillo, para hacerlo con Docker, se agrega el dockerfile, como el citado anteriormente, y al tener en tu repositorio de github tu Dockerfile, render automáticamente detecta que usarás Docker, por lo que solo debes seguir los pasos como estan en el tutorial, asegurándote que en vez de que este seleccionado python en la parte de runtime, se seleccione Docker.

- Para consumir la API se encuentra en el siguiente link: [https://pi1-ml.onrender.com/](https://pi1-ml.onrender.com/)

## Video

En el siguiente enlace, podemos ver el video de todo el poryecto, donde se hace un brvee recorrido por todos los pasos del proyecto:
(enlace)
