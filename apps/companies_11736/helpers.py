import re
from datetime import timedelta
from time import monotonic


class Timer:
    def __init__(self):
        self.start = None
        self.stop = None

    def __enter__(self):
        self.start = monotonic()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop = monotonic()

    @property
    def elapsed(self) -> timedelta:
        return timedelta(seconds=self.stop - self.start)


def get_managers_json(data):
    roles = re.findall(r'\[(\w+)\]', data)
    names = re.findall(r'(\w+\s\w+)', data)

    if roles:
        return [{'name': name, 'role': role} for name, role in zip(names, roles)]
    return [{'name': name} for name in names]


def get_founders_json(data):
    cots = re.findall(r'\(([^)]+)\)', data)
    names = re.findall(r'(\w+\s\w+)', data)

    if cots:
        return [{'name': name, 'cota': cota} for name, cota in zip(names, cots)]
    return [{'name': name} for name in names]


def get_beneficiaries_json(data):
    countries = re.findall(r'\(([^)]+)\)', data)
    names = re.findall(r'(\w+\s\w+)', data)

    if countries:
        return [{'name': name, 'country': country} for name, country in zip(names, countries)]
    return [{'name': name} for name in names]


def get_activities_json(data):
    activities = re.findall(r'(\d+)', data)
    return [{'id': activity} for activity in activities]


def log_changes(current_data: dict, prev_object: object):
    prev_data = vars(prev_object)

    return {key: value for key, value in current_data.items() if
            key not in ('idno', 'register_date', 'liquidation_date') and prev_data.get(key) != value}


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]
