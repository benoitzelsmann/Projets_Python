from datetime import datetime, timedelta, timezone

import requests


class Meteo:
    def __init__(self):
        """Initialise le client météo pour la ville configurée."""
        self.WEATHER_KEY = "cbc2e1ecf506311714fb01d01dfd3bec"
        self.CITY = "Stockholm"
        self.UNITS = "metric"
        self.LANG = "en"

    def alert_daytime(self, delay: int) -> str:
        """Génère des alertes pluie/neige pour la journée cible (06:00-20:00)."""
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={self.CITY}&appid={self.WEATHER_KEY}&units={self.UNITS}&lang={self.LANG}"
        resp = requests.get(url)
        data = resp.json()

        tomorrow = (datetime.now(timezone.utc) + timedelta(days=delay)).date()

        forecasts = [entry for entry in data["list"] if datetime.fromtimestamp(entry["dt"]).date() == tomorrow]

        if not forecasts:
            return "No forecast for tomorrow."

        alerts = []

        for entry in forecasts:
            dt_local = datetime.fromtimestamp(entry["dt"])
            hour = dt_local.hour
            if 6 <= hour <= 20:  # filtrer entre 6h et 20h
                pluie = entry.get("rain", {}).get("3h", 0)
                neige = entry.get("snow", {}).get("3h", 0)

                if pluie > 0:
                    alerts.append(f"🌧️ Rain at {dt_local.strftime('%H:%M')} - {pluie} mm \n")
                if neige > 0:
                    alerts.append(f"❄️ Snow at {dt_local.strftime('%H:%M')} - {neige} mm \n")

        if not alerts:
            return "☀️ No rain/snow expected tomorrow."

        return "".join(alerts)


if __name__ == "__main__":
    meteo = Meteo()
    for i in range(10):
        print(meteo.alert_daytime(i))
