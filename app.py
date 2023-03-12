# -*- coding: utf-8 -*-
"""
Created on February 2023

@author: Albert ETPX
"""

# Importación de módulos externos
from matplotlib.backend_bases import FigureCanvasBase
import mysql.connector
from flask import Flask, Response, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
# Funciones de backend #############################################################################

# connectBD: conecta a la base de datos users en MySQL


def connectBD():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="MoapetS15",
        database="users"
    )
    return db

# initBD: crea una tabla en la BD users, con un registro, si está vacía


def initBD():
    bd = connectBD()
    cursor = bd.cursor()

    # cursor.execute("DROP TABLE IF EXISTS users;")
    # Operación de creación de la tabla users (si no existe en BD)
    query = "CREATE TABLE IF NOT EXISTS users(\
            user varchar(30) primary key,\
            password varchar(30),\
            name varchar(30), \
            surname1 varchar(30), \
            surname2 varchar(30), \
            age integer, \
            genre enum('H','D','NS/NC')); "
    cursor.execute(query)

    # Operación de inicialización de la tabla users (si está vacía)
    query = "SELECT count(*) FROM users;"
    cursor.execute(query)
    count = cursor.fetchall()[0][0]
    if (count == 0):
        query = "INSERT INTO users \
            VALUES('user01','admin','Ramón','Sigüenza','López',35,'H');"
        cursor.execute(query)

    bd.commit()
    bd.close()
    return

# checkUser: comprueba si el par usuario-contraseña existe en la BD


def checkUser(user, password):
    bd = connectBD()
    cursor = bd.cursor()

    query = f"""SELECT user,name,surname1,surname2,age,genre FROM users WHERE user=%s\
            AND password=%s"""
    params = (user, password)
    cursor.execute(query, params)
    userData = cursor.fetchall()
    bd.close()
    if userData == []:
        return False
    else:
        return userData[0]

# cresteUser: crea un nuevo usuario en la BD


def createUser(user, password, name, surname1, surname2, age, genre):
    bd = connectBD()
    cursor = bd.cursor()
    query_1 = "insert into users (user,password,name,surname1,surname2,age,genre) value (%s,%s,%s,%s,%s,%s,%s)"
    val_1 = user, password, name, surname1, surname2, age, genre
    cursor.execute(query_1, val_1)
    # Serveix per inserir els valors a la taula
    n = cursor.rowcount
    bd.commit()
    bd.close()
    return n


# Secuencia principal: configuración de la aplicación web ##########################################
# Instanciación de la aplicación web Flask
app = Flask(__name__)

# Declaración de rutas de la aplicación web


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    initBD()
    return render_template("login.html")


@app.route("/signin")
def signin():
    return render_template("signin.html")


@app.route("/results", methods=('GET', 'POST'))
def results():
    if request.method == ('POST'):
        formData = request.form
        user = formData['usuario']
        password = formData['contrasena']
        userData = checkUser(user, password)

        if userData == False:
            return render_template("results.html", login=False)
        else:
            return render_template("results.html", login=True, userData=userData)

# Amb aquesta funció el que hem de fer es que els valors que introduim al formulari s'apliquin a la base de dades


@app.route("/newUser", methods=('GET', 'POST'))
def newUser():
    if request.method == ('POST'):
        formData = request.form
        print(formData)
        user = formData['usuari']
        password = formData['contrasenya']
        name = formData['nom']
        surname1 = formData['cognom1']
        surname2 = formData['cognom2']
        age = formData['edat']
        genre = formData['genere']
        userData = createUser(user, password, name,
                              surname1, surname2, age, genre)
        if userData == True:
            return render_template("home.html")
        else:
            return render_template("home.html")


# Configuración y arranque de la aplicación web
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(host='localhost', port=5000, debug=True)

################# Espai dedicat a l'analisi de les dades i creació del gràfic #################


def llegir_arxiu():
    fitxer = open('Recurços/seriespoblacionales.csv',
                  mode='r', encoding='UTF-8')
    info_poblacio_2022 = fitxer.readlines()
    # print(info_poblacio_2022)
    fitxer.close()
    return info_poblacio_2022


info_poblacio = []
info_poblacio_2022 = llegir_arxiu()
info_poblacio_2022.pop(0)
info_poblacio += info_poblacio_2022

info_poblacio_neta = []
for linia in info_poblacio_2022:
    linia = linia.replace("�", "n")
    linia = linia.replace("\n", "")
    linia = linia.replace(".", "")
    personesxedat = linia.split(";")
    info_poblacio_neta.append(personesxedat)
info_poblacio = info_poblacio_neta
# Aquest petit trosset de codi es pot aprofitar per a les dos funcións ja que l'eix y no varia


def analitzar_edat(any, genere):
    info_poblacio_edat = []
    for linia in info_poblacio:
        if linia[3] == any and linia[2] == genere and linia[1] == "Espanoles":
            info_poblacio_edat.append(
                linia[0])

    # print(info_poblacio_edat)
    return (info_poblacio_edat)

# També ha sigut necessari netejar els punts en els nombres degut a que principalment és de tipus string i per a que el gràfic utilitzés bé les dades calía que estiguessin en numero(Int/Float)
################################## Analitzar les dades per homes ################################################


def analitzar_quantitat_homes(any, genere):
    info_poblacio_quantitat = []
    for linia in info_poblacio:
        if linia[3] == any and linia[2] == genere and linia[1] == "Espanoles":
            info_poblacio_quantitat.append(linia[4])
            int_poblacio_quantitat = list(map(int, info_poblacio_quantitat))
    # print(info_poblacio_quantitat)
    return (int_poblacio_quantitat)
################################## Analitzar les dades per dones ################################################


def analitzar_quantitat_dones(any, genere):
    info_poblacio_quantitat = []
    for linia in info_poblacio:
        if linia[3] == any and linia[2] == genere and linia[1] == "Espanoles":
            info_poblacio_quantitat.append(linia[4])
            int_poblacio_quantitat = list(map(int, info_poblacio_quantitat))
    # print(info_poblacio_quantitat)
    return (int_poblacio_quantitat)


#################################################################################################################
@app.route("/grafic", methods=('GET', 'POST'))
def grafico():
    # Ja tenim un gràfic horitzontal, això ho aconseguim utilitzant el plt.barh
    # Aqui cridem a les funcions amb les dades predeterminades any=2022 i genere=Home
    info_poblacio_edat_homes = analitzar_edat("2022", "Hombres")
    int_poblacio_quantitat_homes = analitzar_quantitat_homes("2022", "Hombres")
    # Aqui cridem a les funcions amb les dades predeterminades any=2022 i genere=Dona
    info_poblacio_edat_dones = analitzar_edat("2022", "Mujeres")
    int_poblacio_quantitat_dones = analitzar_quantitat_dones("2022", "Mujeres")
    #################################################################################################################
    #  Hem creat el dataframe amb les dos llistes de la variable Homes
    registre_de_dades_homes = {"Franja d'edat": info_poblacio_edat_homes,
                               "Nombre de persones": int_poblacio_quantitat_homes}
    df_homes = pd.DataFrame(registre_de_dades_homes)
    #  Hem creat el dataframe amb les dos llistes de la variable Dones
    registre_de_dades_dones = {"Franja d'edat": info_poblacio_edat_dones,
                               "Nombre de persones": int_poblacio_quantitat_dones}
    df_dones = pd.DataFrame(registre_de_dades_dones)
    #  LLavors amb .iloc el que fem és organitzar de forma manual l'index tant homes com dones
    df_homes = df_homes.iloc[[19, 0, 1, 2, 3, 4, 5, 6, 7, 9,
                              10, 11, 12, 13, 14, 15, 16, 17, 18, 8, 20]]
    df_dones = df_dones.iloc[[19, 0, 1, 2, 3, 4, 5, 6, 7, 9,
                              10, 11, 12, 13, 14, 15, 16, 17, 18, 8, 20]]

    def crear_grafico_barras():
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        axs[0].barh(df_homes["Franja d'edat"], df_homes["Nombre de persones"])
        axs[0].set_title("Població masculina espanyola per edat al 2022")
        axs[0].invert_xaxis()
        axs[0].invert_yaxis()
        axs[1].barh(df_dones["Franja d'edat"], df_dones["Nombre de persones"])
        axs[1].set_title("Població femenina espanyola per edat al 2022")
        axs[1].invert_yaxis()
        plt.show()
        mpld3.show()
        return plt.gcf()
    # Genera el gráfico de barras
    grafico = crear_grafico_barras()
    # Convierte el gráfico en un objeto HTML
    grafico_html = mpld3.fig_to_html(grafico)
    # Retorna la plantilla con el objeto HTML de la gráfica
    return render_template("grafic.html", grafico_html=grafico_html)


if __name__ == "__main__":
    app.run(debug=True)
