from GetEvents import GetEvents
from Notifier import Notifier
from Meteo import Meteo


def main() -> None:
    """Point d'entrée: récupère événements et météo puis envoie une notification."""
    time_planner = GetEvents()
    notifier = Notifier()
    meteo = Meteo()

    delay = 1

    events = time_planner.get_events_delay(delay)
    alert = meteo.alert_daytime(delay)

    notifier.notify(events + "\n\n" + alert)


if __name__ == "__main__":
    main()
