import pandas as pd
import matplotlib.pyplot as plt
import mpld3
import json


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

fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].barh(df_homes["Franja d'edat"], df_homes["Nombre de persones"])
axs[0].set_title("Població masculina espanyola per edat al 2022")
axs[0].invert_xaxis()
axs[0].invert_yaxis()
axs[1].barh(df_dones["Franja d'edat"], df_dones["Nombre de persones"])
axs[1].set_title("Població femenina espanyola per edat al 2022")
axs[1].invert_yaxis()
plt.savefig("grafic.png")
plt.show()
