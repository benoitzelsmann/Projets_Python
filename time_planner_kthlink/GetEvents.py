from datetime import datetime, time, timedelta
from RoomFinder import RoomFinder

import pytz
import requests
from icalendar import Calendar


class GetEvents:
    def __init__(self):
        self.calendar_link = "https://calendar.google.com/calendar/ical/scube14lja2ootld66l9h7c0896sjg8p%40import.calendar.google.com/public/basic.ics"
        self.response = requests.get(self.calendar_link)
        self.calendar = Calendar.from_ical(self.response.content)
        self.tz = pytz.timezone('Europe/Paris')
        self.room_finder = RoomFinder()

    @staticmethod
    def shorten_title(title: str) -> str:
        mapping = {
            "IL2246": "Analog and Digital Electronics",
            "EJ2301": "Power Electronics",
        }
        for long, short in mapping.items():
            if long.lower() in title.lower():
                return short
        return title

    @staticmethod
    def safe_decode(value) -> str:
        if isinstance(value, bytes):
            try:
                return value.decode("utf-8")
            except UnicodeDecodeError:
                return value.decode("latin-1")
        return str(value)

    @staticmethod
    def extract_type(summary: str) -> str:
        mapping = {"foreläsning": "CM",
                   "övning": "TD",
                   "exercice": "TD",
                   "lecture": "CM",
                   "laboration": "LAB"}
        for key, value in mapping.items():
            if key in summary.lower():
                return value
        return ""

    def events_of_day(self, day: datetime) -> list:
        if day is None:
            day = datetime.now()
        start_of_day = self.tz.localize(datetime.combine(day.date(), time.min))
        end_of_day = self.tz.localize(datetime.combine(day.date(), time.max))
        events_in_day = []

        for ev in self.calendar.walk("VEVENT"):
            start = ev.decoded('dtstart')
            end = ev.decoded('dtend')

            start = self.tz.localize(start) if start.tzinfo is None else start.astimezone(self.tz)
            end = self.tz.localize(end) if end.tzinfo is None else end.astimezone(self.tz)

            if start <= end_of_day and end >= start_of_day:
                events_in_day.append(ev)

        events_in_day.sort(key=lambda event: event.decoded("dtstart"))

        return events_in_day

    def decode_events(self, events) -> list:
        decoded = []
        for ev in events:
            summary = self.safe_decode(ev.decoded('summary'))
            start = ev.decoded('dtstart')
            end = ev.decoded('dtend')
            start = self.tz.localize(start) if start.tzinfo is None else start.astimezone(self.tz)
            end = self.tz.localize(end) if end.tzinfo is None else end.astimezone(self.tz)

            location = self.safe_decode(ev.decoded('location')) if ev.get('location') else "No place"

            room_url, map_url = (None, None)
            if location and location != "No place":
                try:
                    room_url, map_url = self.room_finder.find_room_json(location)
                except Exception:
                    pass

            decoded.append({
                "Title": self.shorten_title(summary),
                "Type": self.extract_type(summary),
                "Location": location,
                "RoomURL": room_url,
                "MapURL": map_url,
                "Start": start,
                "End": end,
                "Description": self.safe_decode(ev.decoded('description')) if ev.get('description') else ""
            })

        return decoded

    def get_events_day(self, day: datetime) -> str:
        events = self.decode_events(self.events_of_day(day))
        if not events:
            return f"*No events found for {day.strftime('%A %d %B %Y')}*"

        lines = [f"*📅 {day.strftime('%A %d %B %Y')}*\n"]
        for ev in events:
            title_line = f"➡️ [[{ev['Type']}]] *{ev['Title']}*" if ev['Type'] else f"➡️ *{ev['Title']}*"

            # Lieu : avec lien cliquable et maps
            if ev["RoomURL"]:
                loc_line = f"[{ev['Location']}]({ev['RoomURL']})"
                if ev["MapURL"]:
                    loc_line += f" -> [Map]({ev['MapURL']})"
            else:
                loc_line = ev["Location"]

            block = (
                f"{title_line}\n"
                f"   🕒 *{ev['Start'].strftime('%H:%M')}* - *{ev['End'].strftime('%H:%M')}*\n"
                f"   📍 {loc_line}\n"
            )
            if ev['Description'].strip():
                block += f"   📝 [Course Info]({ev['Description'].splitlines()[0]})\n"
            lines.append(block)
        return "\n".join(lines) + "\n"

    def get_events_delay(self, delay: int) -> str:
        return self.get_events_day(datetime.now() + timedelta(days=delay))
