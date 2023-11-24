from fastapi import FastAPI
import pandas as pd

app = FastAPI()

dff1=pd.read_csv('Función_PlayTimeGenre.csv')
dff2=pd.read_csv('Función_UserForGenre.csv')
dff3=pd.read_csv('Función_UsersRecommend.csv')
dff4=pd.read_csv('Función_UsersWorstDeveloper.csv')
dff5=pd.read_csv('Función_sentiment_analysis.csv')
dff6=pd.read_csv('consulta_modelo1.csv')
#dff3['Año_review']=pd.to_datetime(dff3.Año_review)
listaf1=dff1.Género.unique().tolist()
listaf2=dff2.Género.unique().tolist()
listaf3=dff3.Año_review.unique().tolist()
listaf4=dff4.Año_review.unique().tolist()
listaf5=dff5.Desarrollador.tolist()
listaf6=[dff6[['Id_juego','Nombre']]]
@app.get("/")
def bienvenido():
    mensaje='Bienvenido a la api, ingresa alguna de las siguientes funciones: - PlayTimeGenre/género buscado, - UserForGenre/género buscado'
    return mensaje

@app.get("/PlayTimeGenre/{genero}")
def PlayTimeGenre(genero : str):
    dict={}
    genero=genero.capitalize()
    if genero not in listaf1:
        return f'Por favor ingrese un género válido de la siguiente lista:{listaf1}'
    mensaje="Año de lanzamiento con más horas jugadas para Género "+genero
    dict[mensaje]=dff1.Año[dff1['Género']==genero].iloc[0]
    return dict

@app.get("/UserForGenre/{genero}")
def UserForGenre(genero : str):
    genero=genero.split(' ')
    genero=[a.capitalize()+" " for a in genero]
    genero=''.join(genero)
    genero=genero.strip()
    if genero not in listaf2:
        return f'genero mal {genero},Por favor ingrese un género válido de la siguiente lista:{listaf2}'
    l1=[]
    for a in dff2.loc[dff2.Género==genero,'Año']:
        if dff2.loc[(dff2.Año==a)&(dff2.Género==genero),'Horas_jugadas'].iloc[0]==0:
            continue
        else:
            horas=dff2.loc[(dff2.Año==a)&(dff2.Género==genero),'Horas_jugadas'].iloc[0]
            l1.append({'Año':int(a),'Horas':horas})
    usuario=dff2.Id_usuario[dff2.Género==genero].unique()[0]
    return usuario

@app.get("/UsersRecommend/{anio}")
def UsersRecommend( anio : int):
    año=anio
    if año not in listaf3:
        return f'Por favor ingresa un año de la siguiente lista: {listaf3}'
    l=[]
    for a in range(3):
        dict={f'Puesto {a+1}':dff3[dff3.Año_review==año].iloc[a,0]}
        l.append(dict)
    return l

@app.get("/UsersWorstDeveloper/{anio}")
def UsersWorstDeveloper( anio : int):
    año=anio
    if año not in listaf4:
        return f'Por favor ingresa un año de la siguiente lista: {listaf4}'
    dict={}
    for a,b in enumerate(dff4.loc[dff4.Año_review==año,'Desarrollador']):
        dict['Puesto '+str(a+1)]=b
    return dict

@app.get("/sentiment_analysis/{empresa_desarrolladora}")
def sentiment_analysis( empresa_desarrolladora : str): 
   if empresa_desarrolladora not in listaf5:
       return f'Por favor ingresa una empresa de la siguiente lista: {listaf5}'
   Negative=dff5.sentiment_analysis_0[dff5.Desarrollador==empresa_desarrolladora].iloc[0]
   Neutral=dff5.sentiment_analysis_1[dff5.Desarrollador==empresa_desarrolladora].iloc[0]
   Positive = dff5.sentiment_analysis_2[dff5.Desarrollador==empresa_desarrolladora].iloc[0]
   l= f'[Negative = {Negative}, Neutral =  {Neutral}, Positive = {Positive}]'
   return {empresa_desarrolladora:l}

@app.get("/recomendacion_juego/{id_de_producto}")
def recomendacion_juego( id_de_producto : int):
    if id_de_producto not in listaf6[0]['Id_juego'].to_list():
        l=[('Id: ',dff6.Id_juego[a],'Nombre: ',dff6.Nombre[a]) for a in range(len(dff6[['Id_juego','Nombre']]))]
        return f'por favor ingrese un id de las siguiente lista:    {l}'
    return dff6.juegos[dff6.Id_juego==id_de_producto]
