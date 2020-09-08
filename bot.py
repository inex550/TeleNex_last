import requests
from . import types


class Bot:
    def __init__(self, tocken):
        self.tocken: str = tocken
        self.url: str = f'https://api.telegram.org/bot{tocken}/'
        self.last_update: Int = 0

        self.__text_cmds = {}
        self.__stick_cmds = {}
        self.__global_cmds = {}

    def __get_method(self, method: str, params: dict = {}) -> dict:
        response = requests.get(self.url + method, data=params)
        return response.json()

    def __wait_updates(self) -> dict:
        params = {'timeout': 60, 'offset': self.last_update + 1}
        response = requests.get(self.url + 'getUpdates', data=params)
        response = response.json()
        updates = response['result']
        return updates

    def __process_message(self, json_msg: dict):
        msg = types.Message(json_msg)

        if 'all' in self.__global_cmds:
            self.__global_cmds['all'](msg)

        if msg.text:
            if 'text' in self.__global_cmds:
                self.__global_cmds['text'](msg)

            lower_text = msg.text.lower()

            if lower_text in self.__text_cmds:
                if self.__text_cmds[lower_text].reg == True:
                    self.__text_cmds[lower_text].func(msg)

                elif msg.text == self.__text_cmds[lower_text].orig:
                    self.__text_cmds[lower_text].func(msg)

        if msg.sticker:
            if 'sticker' in self.__global_cmds:
                self.__global_cmds['sticker'](msg)

            if msg.sticker.file_id in self.__stick_cmds:
                self.__stick_cmds[msg.sticker.file_id](msg)

    def send_msg(self, chat_id: int, text: str):
        self.__get_method('sendMessage', {'chat_id': chat_id, 'text': text})

    def send_sticker(self, chat_id: int, stick: str):
        self.__get_method('sendSticker', {'chat_id': chat_id, 'sticker': stick})

    def on_message(
            self, 
            text: str     = None, 
            texts: list   = None, 
            cmds: list    = None, 
            msg_type: str = None,
            stickers: str = None,
            reg: bool     = True
        ):

        def decorator(func):
            if text:
                self.__text_cmds[text.lower()] = types._TextCmdOpt(func, reg, text)

            if texts:
                for msg in texts:
                    self.__text_cmds[msg.lower()] = types._TextCmdOpt(func, reg, msg)
            
            if cmds:
                for cmd in cmds:
                    cmd = '/' + cmd.split()[0]
                    self.__text_cmds[cmd.lower()] = types._TextCmdOpt(func, False, cmd)

            if stickers:
                for sticker in stickers:
                    self.__stick_cmds[sticker] = func

            if msg_type:
                self.__global_cmds[msg_type] = func

        return decorator

    def run(self):
        while True:
            updates = self.__wait_updates()

            for update in updates:
                if 'message' in update:
                    self.__process_message(update['message'])

                self.last_update = update['update_id']