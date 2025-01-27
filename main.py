import requests, json, os
from pystyle import Colors, Colorate, Center
from utils.funictions import *

version = 1 # NE PAS MODIFIER
text = """
                        ▄▄    ▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄ ▄▄▄▄▄▄▄ 
                        █  █  █ █       █       █       █  █▄█  █       █  █ █  █   █       █
                        █   █▄█ █    ▄▄▄█    ▄  █  ▄▄▄▄▄█       █   ▄   █  █▄█  █   █    ▄▄▄█
                        █       █   █▄▄▄█   █▄█ █ █▄▄▄▄▄█       █  █ █  █       █   █   █▄▄▄ 
                        █  ▄    █    ▄▄▄█    ▄▄▄█▄▄▄▄▄  █       █  █▄█  █       █   █    ▄▄▄█
                        █ █ █   █   █▄▄▄█   █    ▄▄▄▄▄█ █ ██▄██ █       ██     ██   █   █▄▄▄ 
                        █▄█  █▄▄█▄▄▄▄▄▄▄█▄▄▄█   █▄▄▄▄▄▄▄█▄█   █▄█▄▄▄▄▄▄▄█ █▄▄▄█ █▄▄▄█▄▄▄▄▄▄▄█

"""

status = check_code_version(version)
if status == True:
    os.system("cls")
    print("\n")
    print(Colorate.Vertical(Colors.blue_to_white, text, 1))
    print(Center.XCenter("Pour le moment, cet outil ne supporte que les films."))
    print(Center.XCenter("Je ferais un support pour les séries si j'ai pas la flemme"))

    film = input(Colors.blue + "\n[" + Colors.white + "$" + Colors.blue + "]" + Colors.white + " Entrez le film à rechercher: ")
    download_by_title(film)