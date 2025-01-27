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
            background-color: #1a1a1a;
            color: #f0f0f0;
            font-family: 'Poppins', sans-serif;
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
        background: linear-gradient(90deg, #6a11cb, #2575fc);
        color: white;
        padding: 20px 0;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
        border-radius: 0 0 15px 15px;
    }}
        .container {{
            background: rgba(30, 30, 30, 0.9);
            padding: 30px;
            border-radius: 15px;
            width: 90%;
            max-width: 800px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
            text-align: center;
        }}
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            color: #ff6f61;
        }}
        p {{
            font-size: 1.1rem;
            margin: 10px 0;
            color: #b3b3b3;
        }}
        iframe {{
            width: 100%;
            height: 450px;
            border: none;
            border-radius: 10px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
            margin-top: 20px;
        }}
        .copy-btn {{
            display: inline-flex;
            align-items: center;
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            border: none;
            color: white;
            padding: 10px 20px;
            font-size: 1rem;
            font-weight: bold;
            border-radius: 25px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            margin-top: 20px;
            transition: all 0.3s ease;
        }}
        .copy-btn:hover {{
            transform: scale(1.1);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.5);
        }}
        .copy-btn svg {{
            margin-right: 8px;
        }}
        footer {{
            margin-top: 25px;
            font-size: 1rem;
            color: #b3b3b3;
        }}
    </style>
</head>
<body>
    <header>NepsMovie</header>
    <div class="container">
        <h1>{selected_movie['title']}</h1>
        <p class="info">Sortie : <span>{selected_movie['release_date'][:4]}</span></p>
        <p class="info">Note : <span>{selected_movie['vote_average']}/10</span></p>
        <iframe id="player" src="{link}" allowfullscreen></iframe>
        <button class="copy-btn" onclick="copyToClipboard()">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="20" height="20">
                <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 7.5v9m0 0v.01M7.5 7.5v-.01M16.5 7.5v9m0 0v.01M16.5 7.5v-.01M3 12h18m-9-9v18" />
            </svg>
            Copier le lecteur
        </button>
        <footer>Lecteur intégré - {selected_movie['title']}</footer>
    </div>
    <script>
        function copyToClipboard() {{
            const playerIframe = document.getElementById('player').outerHTML;
            navigator.clipboard.writeText(playerIframe)
                .then(() => alert('Le lien du lecteur a été copié dans le presse-papiers.'))
                .catch(err => alert('Une erreur est survenue lors de la copie.'));
        }}
    </script>
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
