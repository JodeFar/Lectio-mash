
from pathlib import Path
import sqlite3
from webbrowser import open
import socket
from flask import Flask, render_template, request
from base64 import b64encode
from random import randint
from waitress import serve
from os import path

print("kom igennem imports \n\n")




def resource_path(sti):
    return (path.dirname(path.realpath(__file__))+fr"\{sti}")











template_dir = resource_path(r"\templates")
static_path = resource_path("static")



app = Flask(__name__, template_folder=template_dir)

app_root = Path(app.root_path)


print(app_root, "urllib ")
app.static_folder = static_path


encodeing = {"1":"ild", "2":"skole", "3":"pukkel", "4":"silver", "5":"kongo", "6":"rex", "7":"cykel", "8":"abe", "9":"import", "0":"FCK", "-":"2200"}
decodeing = {"ild":"1", "skole":"2", "pukkel":"3", "silver":"4", "kongo":"5", "rex":"6", "cykel":"7", "abe":"8", "import":"9", "FCK":"0", "2200":"-"}



conn = sqlite3.connect(resource_path("lectio-database.db"), check_same_thread=False)
c = conn.cursor()


piger = False
heling_dict = {True:None, False:"m"}
piger_dict = {"False":True, "True":False}
bevar_dict = {"False":False, "True":True}

@app.route("/", methods=["POST", "GET"])
def base(piger=False):
    global ip

    if request.method == "POST":
        skifter = request.get_data().decode("utf-8")
        if skifter.split("=")[1] == "skift":
            try:
                piger = skifter.split("=")[0]
                piger = piger_dict[piger]
            except:
                pass
        else:
            try:
                piger = request.get_data().decode("utf-8")
                piger = piger.split("=")[0].split("%21")[1]
                piger = bevar_dict[piger]
            except:
                print("problemer med at forstå bevare dataen om køn")
                piger = False
        try: #ændre tallene
            string_med_ider = request.get_data().decode("utf-8") #får stringen
            string_med_ider = string_med_ider.split("%21")[0] #fjerner venstre
            string_med_ider = ("".join([decodeing.get(x) for x in string_med_ider.split("%2C")]))
            id_1, id_2 = string_med_ider.split("-")
            update_elo(id_1, id_2, id_1)
            print("elo updateret")
        except:
            print("modtog 'skift' eller manipuleret tal")
            pass
    #print("opfinder ider \n\n")
    id_1, id_2 = lav_ider(piger)
    #print("laver værdier \n\n")
    verdi_1 = ",".join(list(map(encodeing.get, (str(id_1) + "-" + str(id_2))))) + "!" + str(piger)
    verdi_2 = ",".join(list(map(encodeing.get, (str(id_2) + "-" + str(id_1))))) + "!" + str(piger)
    #print("får billder der svare til iderne \n\n")
    image_1, image_2 = get_billder(id_1, id_2)

    return render_template("base.html", image_1=image_1, image_2=image_2, navn_1=verdi_1, navn_2=verdi_2, køn=piger, ip=ip)




def lav_ider(piger):
    global database_lenth
    id_1 = (0, 1)
    id_2 = (0, 1)
    while id_1[1] != heling_dict[piger]:
        c.execute(f"SELECT id, køn FROM Personer WHERE id={randint(1, database_lenth)}")
        id_1 = c.fetchone()
    while id_2[1] != heling_dict[piger]:
        c.execute(f"SELECT id, køn FROM Personer WHERE id={randint(1, database_lenth)}")
        id_2 = c.fetchone()
    return id_1[0], id_2[0]



def get_billder(id_1, id_2):
    c.execute(f"SELECT Image FROM Personer WHERE id={id_1}")
    image_1 = c.fetchone()

    c.execute(f"SELECT Image FROM Personer WHERE id={id_2}")
    image_2 = c.fetchone()

    image_1 = b64encode(image_1[0]).decode("utf-8")
    image_2 = b64encode(image_2[0]).decode("utf-8")
    return image_1, image_2



def update_elo(id_1, id_2, vinder_id): #skriver til databasen og opdatere eloen.
    id_1_ny_elo, id_2_ny_elo = calulate_elo(id_1, id_2, vinder_id)
    c.execute("""UPDATE Personer SET elo = :elo WHERE id=:id""", {"id":id_1, "elo":id_1_ny_elo})
    c.execute("""UPDATE Personer SET elo = :elo WHERE id=:id""", {"id":id_2, "elo":id_2_ny_elo})
    conn.commit()

def calulate_elo(id_1, id_2, vinder_id): #beregner eloen for [id_1, id_2, idet_på_vinder]
    k = 32
    elo_1, elo_2 = get_spiller_elo(id_1, id_2)

    elo_t_1 = 10 ** (elo_1 / 400)
    elo_t_2 = 10 ** (elo_2 / 400)

    expexted_win_1 = elo_t_1 / (elo_t_1 + elo_t_2)
    expexted_win_2 = elo_t_2 / (elo_t_1 + elo_t_2)
    if id_1 == vinder_id:
        ny_elo_1 = elo_1 + k * (1 - expexted_win_1)
        ny_elo_2 = elo_2 + k * (0 - expexted_win_2)
        return  round(ny_elo_1), round(ny_elo_2)

    elif id_2 == vinder_id:
        ny_elo_2 = elo_1 + k * (1 - expexted_win_1)
        ny_elo_1 = elo_2 + k * (0 - expexted_win_2)
        return  round(ny_elo_1), round(ny_elo_2)



def get_spiller_elo(id_1,id_2): #giver eloen på to spiller i formen spiller_1 spiller_2
    c.execute(f"SELECT * FROM Personer WHERE id={id_1} OR id={id_2}") #
    elo_list = c.fetchall()
    return elo_list[0][1], elo_list[1][1]


def get_ip():
    print("vca")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


ip = get_ip() + ":4000/"


c.execute("SELECT id from Personer;")
database_lenth = len(c.fetchall())




if __name__ == "__main__":
    open(f"http://localhost:4000/")

    serve(app, host="0.0.0.0", port="4000", threads=1)
    #app.run(debug=True, host="0.0.0.0")




