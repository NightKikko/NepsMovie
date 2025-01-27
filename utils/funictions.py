import os
from pystyle import Colors
import requests
import re
import json
from fake_useragent import UserAgent


def is_url(input_text):
    pattern = r'^https?://[\w.-]+(?:\.[\w\.-]+)+[/\w\.-]*$'
    return bool(re.match(pattern, input_text))


def clean_filename(text):
    return re.sub(r'[<>:"/\\|?*\(\)]', '_', text)


def download_by_title(film):
    ua = UserAgent()
    url = f"https://frembed.live/api/public/search?query={film}&page=1"
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "movies" in data:
            movies = data["movies"]
        else:
            print(Colors.blue + "\n[" + Colors.white + "!" + Colors.blue + "] " +
                  Colors.white + "Aucun film trouvé pour votre recherche.")
            return

        if not movies:
            print(Colors.blue + "\n[" + Colors.white + "!" + Colors.blue + "] " +
                  Colors.white + "Aucun film trouvé pour votre recherche.")
            return

        print(Colors.blue + "\n[" + Colors.white + "*" + Colors.blue + "] " +
              Colors.white + "Films trouvés :")
        for i, movie in enumerate(movies, start=1):
            print(
                Colors.blue + "[" + Colors.white + str(i) + Colors.blue + "] " +
                Colors.white + f"{movie['title']} ({movie['release_date'][:4]}) - " +
                f"Note: {movie['vote_average']}/10"
            )


        choice = input(Colors.blue + "\n[" + Colors.white + "$" + Colors.blue + "]" + Colors.white +
                       " Entrez le numéro du film que vous souhaitez télécharger : ")

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(movies):
                selected_movie = movies[choice - 1]
                movie_id = selected_movie['id']

                print(
                    Colors.blue + "\n[" + Colors.white + "!" + Colors.blue + "]" +Colors.white + " Vous avez sélectionné : " + Colors.white +
                    f"{selected_movie['title']} ({selected_movie['release_date'][:4]})"
                )
                player_url = f"https://api.frembed.lol/movies/check?id={movie_id}"
                player_response = requests.get(player_url, headers=headers)

                if player_response.status_code == 200:
                    player_data = player_response.json()
                    if player_data["status"] == 200 and player_data["result"]["Total"] > 0:
                        link = player_data["result"]["items"][0]["link"]

                        output_dir = os.path.join(os.path.dirname(__file__), '../films')
                        os.makedirs(output_dir, exist_ok=True)

                        title = clean_filename(selected_movie['title']).replace(" ", "_")
                        file_name = os.path.join(output_dir, f"{title}.html")
                        html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{selected_movie['title']} - Lecteur</title>
    <style>
        body {{
            background: #f4f4f9;
            color: #333;
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }}
        header {{
            width: 100%;
            background: linear-gradient(90deg, #4cc9f0, #4361ee); 
            color: white;
            padding: 15px 0;
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            position: fixed;
            top: 0;
            left: 0;
            z-index: 10;
            border-bottom: 3px solid #4361ee;
        }}
        iframe {{
            width: 100%;
            height: 400px;
            border: none;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            margin-top: 15px;
        }}
    </style>
</head>
<body>
    <header>NepsMovie</header>
    <div class="container">
        <h1>{selected_movie['title']}</h1>
        <iframe src="{link}" allowfullscreen></iframe>
    </div>
</body>
</html>
                        """

                        file_name = f"films/{title}.html"
                        with open(file_name, "w", encoding="utf-8") as file:
                            file.write(html_content)
                        print(Colors.blue + "\n[" + Colors.white + "*" + Colors.blue + "] " +
                              Colors.white + f"Le fichier HTML a été généré : {file_name}")
                    else:
                        print(Colors.blue + "\n[" + Colors.white + "!" + Colors.blue + "] " +
                              Colors.white + "Aucun lecteur disponible pour ce film.")
                else:
                    print(Colors.blue + "\n[" + Colors.white + "!" + Colors.blue + "] " +
                          Colors.white + "Erreur lors de la récupération des lecteurs.")
            else:
                print(Colors.blue + "\n[" + Colors.white + "!" + Colors.blue + "] " +
                      Colors.white + "Choix invalide. Aucun film sélectionné.")
        else:
            print(Colors.blue + "\n[" + Colors.white + "!" + Colors.blue + "] " +
                  Colors.white + "Entrée invalide. Veuillez entrer un numéro.")
    else:
        print(Colors.blue + "\n[" + Colors.white + "!" + Colors.blue + "] " +
              Colors.white + "Erreur lors de la récupération des données. Veuillez réessayer.")


def check_code_version(version): # vérifier la version actuelle du code et prévenir s'il y a une mise à jour
    try:
        response = requests.get('https://raw.githubusercontent.com/NightKikko/NepsMovie/refs/heads/main/version.json')
        data = json.loads(response.text)
        if data['version'] != version:
            print(Colors.blue + "\n[" + Colors.white + "$" + Colors.blue + "]" + Colors.white + " Votre version n'est pas à jour! Merci de le mettre à jour.\nhttps://github.com/NightKikko/NepsMovie/")
            exit()
        return True
    except Exception as e:
        print(Colors.red + f"Une erreur est survenue : {e}")
        exit()
