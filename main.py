from fastapi import FastAPI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

#se cargan los datos desde un csv 
dff1=pd.read_csv('Función_PlayTimeGenre.csv')
dff2=pd.read_csv('Función_UserForGenre.csv')
dff3=pd.read_csv('Función_UsersRecommend.csv')
dff4=pd.read_csv('Función_UsersWorstDeveloper.csv')
dff5=pd.read_csv('Función_sentiment_analysis.csv')
dff6=pd.read_csv('consulta_modelo1.csv')
#creamos listas con datos de años, generos,y desarrollador para cada función
listaf1=dff1.Género.unique().tolist()
listaf2=dff2.Género.unique().tolist()
listaf3=dff3.Año_review.unique().tolist()
listaf4=dff4.Año_review.unique().tolist()
listaf5=dff5.Desarrollador.tolist()
listaf6=[dff6[['Id_juego','Nombre']]]


@app.get("/")
def bienvenido():
    """
    Ruta principal de la aplicación.

    Returns:
        str: Mensaje de bienvenida y descripción de las funciones disponibles.
    """
    userforgenre='/UserForGenre/'
    playtimegenre='/PlayTimeGenre/' 
    usersrecommend='/UsersRecommend/'
    usersworstdeveloper='/UsersWorstDeveloper/'
    sentimentanalysis='/sentiment_analysis/'
    recomendacionjuego= '/recomendacion_juego/'
    mensaje='Bienvenido a la API, ingrese en la barra de navegación al final del url alguna de las siguientes funciones: '
    return mensaje + userforgenre+', ' + playtimegenre + ', ' +usersrecommend + ', ' + usersworstdeveloper + ', ' + sentimentanalysis + ', '+ recomendacionjuego

@app.get("/PlayTimeGenre/")
def Playtiemgenre():

    """Ruta para obtener la lista de géneros disponibles.

    Returns:
        str: Mensaje indicando que se debe ingresar un género válido.
    """ 
    return f'Ingrese en la barra de navegación al final del url el género buscado   --(devuelve el año con mas horas jugadas para dicho género.)      Por favor ingrese un género válido de la siguiente lista:{listaf1}'

@app.get("/PlayTimeGenre/{genero}")
def PlayTimeGenre(genero : str ):
    """
    Ruta para obtener el año de lanzamiento con más horas jugadas para un género específico.

    Args:
        genero (str): Género para el cual se busca la información.

    Returns:
        dict: Diccionario con el año de lanzamiento con más horas jugadas para el género.
    """
       
    dict={}
    genero=genero.capitalize()
    if genero not in listaf1:
        return f'(Por favor ingrese un género válido de la siguiente lista:{listaf1}'
    mensaje="Año de lanzamiento con más horas jugadas para Género " + genero
    dict[mensaje]=dff1.Año_lanzamiento[dff1['Género']==genero].iloc[0]
    return dict

@app.get("/UserForGenre/")
def Userforgenre():
    """
    Ruta para obtener la lista de géneros disponibles.

    Returns:
        str: Mensaje indicando que se debe ingresar un género válido.
    """
    return f'Ingrese en la barra de navegación al final del url el género buscado   --(Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año)      Por favor ingrese un género válido de la siguiente lista:{listaf2}'

@app.get("/UserForGenre/{genero}")
def UserForGenre(genero : str):
    """
    Ruta para obtener el usuario que acumula más horas jugadas para un género y una lista de horas jugadas por año.

    Args:
        genero (str): Género para el cual se busca la información.

    Returns:
        dict: Usuario que acumula más horas jugadas y lista de horas jugadas por año.
    """
    genero=genero.split(' ')
    genero=[a.capitalize()+" " for a in genero]
    genero=''.join(genero)
    genero=genero.strip()
    if genero not in listaf2:
        return f'género erróneo {genero}, Por favor ingrese un género válido de la siguiente lista:{listaf2}'
    l1=[]
    for a in dff2.loc[dff2.Género==genero,'Año_lanzamiento']:
        if dff2.loc[(dff2.Año_lanzamiento==a)&(dff2.Género==genero),'Horas_jugadas'].iloc[0]==0:
            continue
        else:
            horas=dff2.loc[(dff2.Año_lanzamiento==a)&(dff2.Género==genero),'Horas_jugadas'].iloc[0]
            l1.append({'Año':a,'Horas':horas})
    usuario=dff2.Id_usuario[dff2.Género==genero].unique()[0]
    return usuario

@app.get("/UsersRecommend/")
def Usersrecommend():
    """
    Ruta para obtener la lista de años disponibles.

    Returns:
        str: Mensaje indicando que se debe ingresar un año válido.
    """
    return f'Ingrese en la barra de navegación al final del url el año buscado.    --Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.    --Por favor ingresa un año de la siguiente lista: {listaf3}'

@app.get("/UsersRecommend/{anio}")
def UsersRecommend( anio : int):
    """
    Ruta para obtener el top 3 de juegos más recomendados por usuarios para un año dado.

    Args:
        anio (int): Año para el cual se busca la información.

    Returns:
        list: Lista con el top 3 de juegos más recomendados.
    """
    año=anio
    if año not in listaf3:
        return f'Por favor ingresa un año de la siguiente lista: {listaf3}'
    l=[]
    for a in range(3):
        dict={f'Puesto {a+1}':dff3[dff3.Año_review==año].iloc[a,0]}
        l.append(dict)
    return l

@app.get("/UsersWorstDeveloper/")
def Usersworstdeveloper():
    """
    Ruta para obtener la lista de años disponibles.

    Returns:
        str: Mensaje indicando que se debe ingresar un año válido.
    """
    return f'Ingrese en la barra de navegación al final del url el año buscado.     --(Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado.    --Por favor ingresa un año de la siguiente lista: {listaf4}'

@app.get("/UsersWorstDeveloper/{anio}")
def UsersWorstDeveloper( anio : int):
    """
    Ruta para obtener el top 3 de desarrolladoras con juegos menos recomendados por usuarios para un año dado.

    Args:
        anio (int): Año para el cual se busca la información.

    Returns:
        dict: Diccionario con el top 3 de desarrolladoras con juegos menos recomendados.
    """
    año=anio
    if año not in listaf4:
        return f'Por favor ingresa un año de la siguiente lista: {listaf4}'
    dict={}
    for a,b in enumerate(dff4.loc[dff4.Año_review==año,'Desarrollador']):
        dict['Puesto '+str(a+1)]=b
    return dict


@app.get("/sentiment_analysis/")
def Sentimentanalysis():
    """
    Ruta para obtener la lista de empresas desarrolladoras disponibles.

    Returns:
        str: Mensaje indicando que se debe ingresar una empresa válida.
    """
    return f'Ingrese en la barra de navegación al final del url la empresa desarrolladora buscada (Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.)   --Por favor ingresa una empresa de la siguiente lista: {listaf5}'

@app.get("/sentiment_analysis/{empresa_desarrolladora}")
def sentiment_analysis( empresa_desarrolladora : str): 
   
    """
    Ruta para obtener el análisis de sentimiento para una empresa desarrolladora.

    Args:
        empresa_desarrolladora (str): Empresa desarrolladora para la cual se busca la información.

    Returns:
        dict: Análisis de sentimiento para la empresa desarrolladora.
    """
    if empresa_desarrolladora not in listaf5:
        return f'Por favor ingresa una empresa de la siguiente lista: {listaf5}'
    Negative=dff5.sentiment_analysis_0[dff5.Desarrollador==empresa_desarrolladora].iloc[0]
    Neutral=dff5.sentiment_analysis_1[dff5.Desarrollador==empresa_desarrolladora].iloc[0]
    Positive = dff5.sentiment_analysis_2[dff5.Desarrollador==empresa_desarrolladora].iloc[0]
    l= f'[Negative = {Negative}, Neutral =  {Neutral}, Positive = {Positive}]'
    return {empresa_desarrolladora:l}

@app.get("/recomendacion_juego/")
def Recomendacionjuego():
    """
    Ruta para obtener la lista de juegos disponibles.

    Returns:
        str: Mensaje indicando que se debe ingresar un ID de juego válido.
    """
    l=[('Id: ',dff6.Id_juego[a],'Nombre: ',dff6.Nombre[a]) for a in range(len(dff6[['Id_juego','Nombre']]))]
    return f'Ingrese en la barra de navegación al final del url el id del juego buscado     --(Ingresando el id de producto recibimos una lista con 5 juegos recomendados similares al ingresado.)     Por favor ingrese un id de las siguiente lista:{l}'

@app.get("/recomendacion_juego/{id_de_producto}")
def recomendacion_juego( id_de_producto : int):
    """
    Ruta para obtener una lista de 5 juegos recomendados similares al juego ingresado.

    Args:
        id_de_producto (int): ID del juego para el cual se busca la información.

    Returns:
        list: Lista con 5 juegos recomendados similares.
    """    
    if id_de_producto not in listaf6[0]['Id_juego'].to_list():
        l=[('Id: ',dff6.Id_juego[a],'Nombre: ',dff6.Nombre[a]) for a in range(len(dff6[['Id_juego','Nombre']]))]
        return f'por favor ingrese un id de las siguiente lista:        {l}'
    return dff6.juegos[dff6.Id_juego==id_de_producto]
