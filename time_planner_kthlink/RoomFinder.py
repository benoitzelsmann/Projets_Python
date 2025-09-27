import json

# import requests
# from bs4 import BeautifulSoup


class RoomFinder:
    def __init__(self):

        # with open("rooms.json", "r", encoding="utf-8") as f:
        #     self.room_map = json.load(f)

        pass

    # @staticmethod
    # def find_room_url(room_name: str) -> str | None:
    #     clean_name = room_name.split(",")[0].strip()
    #
    #     search_url = (
    #         f"https://www.kth.se/search?q={clean_name}"
    #         "&entityFilter=kth-place&filterLabel=Facilities&lang=en&btnText="
    #     )
    #
    #     response = requests.get(search_url)
    #     if response.status_code != 200:
    #         return None
    #
    #     soup = BeautifulSoup(response.text, "html.parser")
    #
    #     link = soup.find("a", href=lambda h: h and "/places/room/id/" in h)
    #
    #     return link["href"] if link else None
    #
    # @staticmethod
    # def get_room_map(room_url: str) -> str | None:
    #
    #     response = requests.get(room_url)
    #     if response.status_code != 200:
    #         return None
    #
    #     soup = BeautifulSoup(response.text, "html.parser")
    #
    #     map_link = soup.find("a", href=lambda h: h and "google.com/maps" in h)
    #     if map_link:
    #         return map_link["href"].replace("http", "https")
    #     return None

    # def room_find_kth_server(self, room: str) -> tuple | None:
    #
    #     url = self.find_room_url(room)
    #     map_url = self.get_room_map(url)
    #
    #     return url, map_url

    def find_room_json(self, room: str) -> tuple | None:
        return self.room_map[room]["room_url"], self.room_map[room]["map_url"]



