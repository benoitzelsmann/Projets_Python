import json
from GetEvents import GetEvents
from datetime import datetime, time, timedelta

import requests
from bs4 import BeautifulSoup


class RoomFinder:
    def __init__(self):
        self.getevents = GetEvents()

    @staticmethod
    def find_room_url(room_name: str) -> str | None:
        clean_name = room_name.split(",")[0].strip()
    
        search_url = (
            f"https://www.kth.se/search?q={clean_name}"
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
    
        response = requests.get(room_url)
        if response.status_code != 200:
            return None
    
        soup = BeautifulSoup(response.text, "html.parser")
    
        map_link = soup.find("a", href=lambda h: h and "google.com/maps" in h)
        if map_link:
            return map_link["href"].replace("http", "https")
        return None

    def room_find_kth_server(self, room: str) -> tuple | None:
    
        url = self.find_room_url(room)
        map_url = self.get_room_map(url)
    
        return url, map_url

    def update_rooms(self):



        with open("rooms.json", "r") as rooms_file:
            rooms = json.load(rooms_file)

        new_dic = rooms.copy()

        for day in range(200):
            events = self.getevents.decode_events(self.getevents.events_of_day(datetime.now() + timedelta(days=day)))
            for event in events:

                if event["Location"] not in rooms.keys():
                    print(event["Location"])
                    url, map_url = self.room_find_kth_server(event["Location"])
                    new_dic[event["Location"]] = {"room_url": url, "map_url": map_url}

        json.dump(new_dic, open("rooms.json", "w"))


if __name__ == "__main__":
    RoomFinder().update_rooms()


    


