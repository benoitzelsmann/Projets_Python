import json
from GetEvents import GetEvents
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup





class RoomFinder:
    def __init__(self):
        """Initialise l'outil de recherche de salles."""
        self.getevents = GetEvents()

    @staticmethod
    def find_room_url(room_name: str) -> str | None:
        """Trouve l'URL de la page KTH d'une salle à partir de son nom."""

        search_url = (
            f"https://www.kth.se/search?q={room_name}"
            "&entityFilter=kth-place&filterLabel=Facilities&lang=en&btnText="
        )

        response = requests.get(search_url)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        link = soup.find("a", href=lambda h: h and "/places/room/id/" in h)

        return link["href"] if link else None

    @staticmethod
    def get_room_map(room_url: str) -> str | None:
        """Récupère le lien Google Maps associé à une salle depuis sa page KTH."""
        response = requests.get(room_url)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        map_link = soup.find("a", href=lambda h: h and "google.com/maps" in h)
        if map_link:
            return map_link["href"].replace("http", "https")
        return None

    def room_find_kth_server(self, room: str) -> tuple | None:
        """Trouve l'URL de la salle et son lien Google Maps en interrogeant KTH."""
        url = self.find_room_url(room)

        # ADD THIS CHECK: If no URL was found, return the (None, None) pair immediately.
        if url is None:
            return None, None  # Or you could return None as per your function signature, but (None, None) keeps the return type consistent.

        map_url = self.get_room_map(url)

        return url, map_url

    def update_rooms(self) -> None:
        """Met à jour le fichier rooms.json avec les salles rencontrées dans le calendrier."""

        new_dic = {
            "No place": {
                "room_url": None,
                "map_url": None
            },
        }

        for letter in range(ord('A'), ord('Z') + 1):
            for number in range(0, 80):
                roomkey = chr(letter) + str(number)
                print(roomkey)
                url, map_url = self.room_find_kth_server(roomkey)
                if url is None:
                    continue
                else:
                    print(roomkey + "OK")
                    new_dic[roomkey] = {"room_url": url, "map_url": map_url}

        json.dump(new_dic, open("rooms_tot.json", "w"))

    @staticmethod
    def check_rooms() -> None:
        with open("rooms_tot.json") as file:
            rooms_tot = json.load(file)
        with open("rooms.json") as file:
            rooms = json.load(file)

        keys = [key.split(",")[0] for key in rooms.keys()]
        keys_tot = rooms_tot.keys()

        for key in keys:
            if key not in keys_tot:
                print(key)

    @staticmethod
    def get_room_building_name(room_url: str) -> str | None:
        """
        Récupère le nom du bâtiment (l'adresse) depuis le titre visible
        de la page KTH de la salle.
        """
        try:
            response = requests.get(room_url, timeout=10)
            if response.status_code != 200:
                return None
            soup = BeautifulSoup(response.content, "html.parser")
            title_element = soup.find('h1')
            if not title_element:
                title_element = soup.find('title')

            if title_element:
                full_title_text = title_element.text.strip()
                if ',' in full_title_text:
                    address_part = full_title_text.split(',', 1)[-1].strip()
                else:
                    address_part = full_title_text.split(' - ')[0].strip()

                if address_part:
                    first_line = address_part.split('\n')[0].strip()
                    import re
                    building_name = re.sub(r'[\s,]+\d+[A-Z]?$', '', first_line, count=1).strip()
                    return building_name if building_name else first_line

        except requests.exceptions.RequestException:
            return None

        return None

    # ---

    def room_richer(self) -> None:
        """
        Enrichit les clés du fichier rooms_tot.json en ajoutant le nom du bâtiment
        (l'adresse) à la clé de la salle (ex: "V01" -> "V01, Teknikringen").
        """
        new_rooms_data = {}

        try:
            with open("rooms_tot.json", 'r') as file:
                rooms_tot = json.load(file)
        except FileNotFoundError:
            print("Erreur: Le fichier rooms_tot.json n'a pas été trouvé.")
            return
        except json.JSONDecodeError:
            print("Erreur: Le fichier rooms_tot.json n'est pas un JSON valide.")
            return

        print("Démarrage de l'enrichissement des données de salles...")

        for room_key, room_data in rooms_tot.items():
            room_url = room_data.get("room_url")


            if room_url and room_url != "None":
                # 1. Récupérer le nom du bâtiment
                building_name = RoomFinder.get_room_building_name(room_url)

                if building_name:
                    new_key = f"{room_key}, {building_name}"
                else:
                    new_key = room_key

                print(f"Enrichissement: '{room_key}' -> '{new_key}'")

                # 3. Ajouter à la nouvelle structure
                new_rooms_data[new_key] = room_data
            else:
                # Conserver les salles non trouvées (clé inchangée)
                new_rooms_data[room_key] = room_data

        try:
            with open("rooms_richer.json", 'w') as file:
                json.dump(new_rooms_data, file, indent=2, ensure_ascii=False)
            print("Enrichissement terminé. Les données ont été sauvegardées dans rooms_richer.json.")
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier: {e}")

    # ---



if __name__ == "__main__":
    roomfinder = RoomFinder()
    # roomfinder.update_rooms()
    roomfinder.room_richer()
