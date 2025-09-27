from GetEvents import GetEvents
from Notifier import Notifier
from Meteo import Meteo


def main():
    time_planner = GetEvents()
    notifier = Notifier()
    meteo = Meteo()

    events = time_planner.get_events_delay(1)
    alert = meteo.alert_daytime(1)
    notifier.notify(events + "\n\n" + alert)


if __name__ == "__main__":
    main()
