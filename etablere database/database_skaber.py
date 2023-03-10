from time import sleep
from bs4 import BeautifulSoup
import requests
from re import compile, finditer
from os import path, listdir, mkdir
import sqlite3
from headers_and_cookies import get_headers_and_cookies
from functioner import get_navne_liste, aho_find_index_shared_names


billede_id_liste = []
elev_id_liste = []
id_counter = 0
school_navneliste = []
index = 0

fil_drenge_navne = path.dirname(path.realpath(__file__)) + r"\navne\drengenavne.txt"




data_base_sti = path.dirname(path.dirname(__file__))+r"\main\lectio-database.db"

print("--------------")
print("for at hente den relevante data skal programmet bruge dit lectio:")
headers, cookies = get_headers_and_cookies(input("Brugernavn: "), input("Adgangskode: "))
print("--------------\n")

input("fortsæt?")

pattern = compile(r"\d\d\d\d\d\d\d\d\d\d\d")

print("../",path.dirname(path.realpath(__file__)))





def findnummerelevnummer(elev_id_liste) -> list:
    for x in range(65,91):
        sleep(0.1)
        print(91-x, "turer tilbage")
        source = requests.get(f"https://www.lectio.dk/lectio/{cookies['LastLoginExamno']}/FindSkema.aspx?type=elev&forbogstav={chr(x)}", headers=headers, cookies=cookies).content
        soup = BeautifulSoup(source, "html.parser")
        elev_id_serch = soup.find_all("li")

        elev_id_serch = str(elev_id_serch)
        matches = pattern.finditer(elev_id_serch)

        for index, x in enumerate(matches):
            if index % 2 == 0:
                elev_id_liste.append(x.group())

    return elev_id_liste


def franummertilbillede(Elevnummer):
    sleep(0.1)
    global pattern, headers, cookies, billede_id_liste, school_navne_liste

    source_til_billede = requests.get(f"https://www.lectio.dk/lectio/{cookies['LastLoginExamno']}/SkemaNy.aspx?type=elev&elevid={Elevnummer}",
                                      headers=headers, cookies=cookies).text
    soup = BeautifulSoup(source_til_billede, "html.parser")
    B_ID_serch = str(soup.find("div", class_="thumber"))
    matches = pattern.finditer(B_ID_serch)
    try:
        navn = soup.find('div', {'id': 's_m_HeaderContent_MainTitle'}).text[7:-1].split(" ")[0]
    except:
        print("intet navn uden et billede")
    nummer = 0
    for x in matches:
        nummer = x.group()
    if nummer != 0:
        billede_id_liste.append(nummer)
        school_navneliste.append(navn)




def fra_billedid_til_billed_download():
    sleep(0.1)
    for index, x in enumerate(billede_id_liste):
        with open(f"images\{index}" + '.jpg', 'wb') as f:
            img_url = f"https://www.lectio.dk/lectio/{cookies['LastLoginExamno']}/GetImage.aspx?pictureid={x}&fullsize=1"
            im = requests.get(img_url, cookies=cookies)

            f.write(im.content)



def create_database():  # #laver databasem
    image_database = sqlite3.connect(data_base_sti)
    data = image_database.cursor()

    data.execute('''CREATE TABLE IF NOT EXISTS Personer(
    Image BLOB,
	elo INTEGER,
	id	INTEGER UNIQUE,
	"køn"	TEXT,
	PRIMARY KEY("id"))

    ''')

    image_database.commit()
    image_database.close()


# får den sidstedel af filnavnet og putter dem i filer
def get_files():
    global files
    Dirpath = path.dirname(path.realpath(__file__)) + r"\images"
    files = listdir(Dirpath)


# retunere den fulde filsti på et billede
def get_image_path(file_name):
    Dirpath = path.dirname(path.realpath(__file__)) + r"\images"
    return path.join(Dirpath, file_name)

# bruger den fulde filsti til at lave billede om til binær code
def convert_image_into_binary(filename):
    with open(filename, 'rb') as file:
        photo_image = file.read()
    return photo_image

# indsætter billede i databasen

def insert_image(image):  # image_database = sqlite3.connect(database_sti") #image_database.close()
    global id_counter, image_database
    id_counter += 1
    data = image_database.cursor()
    data.execute("INSERT INTO Personer(Image, elo, id) VALUES(:Image, :elo, :id);", (image, 1400, id_counter))
    image_database.commit()


def insert_gender(id_til_drenge):
    global image_database
    data = image_database.cursor()
    for ide in id_til_drenge:
        data.execute("""UPDATE Personer SET køn = 'm' WHERE id=:id""", {"id": ide+1})
    image_database.commit()





if __name__=="__main__":
    elev_id_liste = findnummerelevnummer(elev_id_liste) #leder efter elev_id_er
    antal_elever = len(elev_id_liste) #finder mængdne af elever



    print("--------------")
    print("påbegynder omdannelsen fra elev_ider til billed_ider")
    print("processen tager ca ", round((antal_elever-index) * 0.09)*2, " sekunder")
    sleep(1)
    print("--------------\n")



    for x in elev_id_liste:
        index += 1
        print(antal_elever-index, "elever tilbage")
        franummertilbillede(x) #får billede fra hver elev




    try:
        mkdir('images')
    except:
        print("kunne ikke lave fil")
        print("dette skyldes højst sansynlig at filen allrede findes hvilket ikke er et problem")

    print("--------------")
    print("downloader alle billeder til en file")
    print("det kan forventes at dette tager nogenlunde den samme mængde tid")
    print("--------------\n")
    fra_billedid_til_billed_download() # downloader alle billeder
    # laver databasen


    create_database()



    print("--------------")
    print("skriver alle billeder ind i en database")
    print("--------------\n")
    image_database = sqlite3.connect(data_base_sti)
    for x in range(len(billede_id_liste)):
        insert_image(convert_image_into_binary(get_image_path(f"{x}.jpg")))

    print("databasen er blevet etableret korrekt")


    drenge_navne = get_navne_liste(fil_drenge_navne)



    ider_til_drenge = aho_find_index_shared_names(drenge_navne,school_navneliste)



    insert_gender(ider_til_drenge)

    #for x in ider_til_drenge: #tjek navne
        #print(school_navneliste[x], x)

    image_database.close()