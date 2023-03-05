from datetime import datetime
from io import TextIOWrapper
import json
import os
import socket


file_name: str = 'data.json'

class Entry:
    def __init__(self) -> None:
        self.datetime: str = self._get_time() 
        self.user: str =  os.environ.get('USER') or 'unknown'
        self.hostname: str = socket.gethostname()

    def to_dict(self) -> dict[str, str]:
        return {
            'datetime': self.datetime,
            'user': self.user,
            'hostname': self.hostname,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def _get_time(self) -> str:
        time = self.round_to_nearest_quarter(datetime.now())
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def round_to_nearest_quarter(self, time: datetime) -> datetime:
        minutes: int = time.minute
        quarter, remainder = divmod(minutes, 15)
        if remainder < 7.5:
            minutes = quarter * 15
        else:
            minutes = (quarter + 1) * 15

        return time.replace(minute=minutes, second=0, microsecond=0) 

def prepare_file() -> None:
    if not os.path.exists(file_name):
        create_empty_file()

def create_empty_file() -> None:
    with open(file_name, 'w') as f:
        json.dump({'entries': []}, f)
        f.close()

def load_data() -> dict[str, list[dict[str, str]]]:
    f: TextIOWrapper = open('data.json', 'r')
    try:
        data: dict[str, list[dict[str, str]]] = json.load(f)
    finally:
        f.close()
    return data

def send_data() -> None:
    print('Sending data to server...')
    success: bool = False
    if success:
        clean_file()

def clean_file() -> None:
    print('Cleaning file...')
    os.remove(file_name)

def main() -> None:
    entry: Entry = Entry()
    prepare_file()
    data = load_data()
    data['entries'].append(entry.to_dict())
    f = open('data.json', 'w')
    json.dump(data, f)

    send_data()

if __name__ == '__main__':
    main()
