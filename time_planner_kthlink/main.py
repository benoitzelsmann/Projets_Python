from GetEvents import GetEvents
from Notifier import Notifier


def main():
    time_planner = GetEvents()
    notifier = Notifier()
    events = time_planner.get_events_delay(1)
    notifier.notify(events)


if __name__ == "__main__":
    main()
