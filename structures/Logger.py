import logging
from datetime import datetime

class Logger:
    def __init__(self, logging_file):
        self.logger = logging.getLogger("MusicBotLogger")
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(logging_file, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, text):
        now = datetime.now()
        info = f"{now.strftime('%H:%M')} - {now.strftime('%d:%m:%Y')} | Info: {text}"
        self.logger.info(info)
        # Exibe no console também, com cores se quiser (opcional)
        print(f"\033[92m{now.strftime('%d:%m:%Y')} - {now.strftime('%H:%M')}\033[0m \033[93m| Info: {text}\033[0m")
