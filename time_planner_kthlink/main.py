from GetEvents import GetEvents
from Notifier import Notifier
from Meteo import Meteo


def main():
    time_planner = GetEvents()
    notifier = Notifier()
    meteo = Meteo()

    delay = 3

    events = time_planner.get_events_delay(delay)
    alert = meteo.alert_daytime(delay)

    notifier.notify(events + "\n\n" + alert)


if __name__ == "__main__":
    main()
