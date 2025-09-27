import requests


class Notifier:
    def __init__(self):
        self.TOKEN = "8317589831:AAFAUc1MguxezYzlSLjazDegdyW-O2eGaLw"
        self.CHAT_ID = "7954099904"
        self.history_filename = "history.json"
        pass

    def __str__(self):
        res = str(type(self).__name__).upper() + '\n'
        for (key, value) in vars(self).items():
            res += f'{key} : {value}\n'
        return res

    # def save_to_history(self, backup):
    #     data = []
    #     if os.path.exists(self.history_filename):
    #         with open(self.history_filename, 'r') as file:
    #             try:
    #                 data = json.load(file)
    #             except json.JSONDecodeError:
    #                 data = []
    #
    #     data.append(backup)
    #
    #     with open(self.history_filename, 'w') as file:
    #         json.dump(data, file, indent=4)

    def notify(self, message):
        url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage"

        params = {"chat_id": self.CHAT_ID,
                  "text": message,
                  "parse_mode": "Markdown",
                  "disable_web_page_preview": True}


        resp = requests.post(url, params=params)
        # self.save_to_history(resp.json())









