import requests
from . import types
import json


class Bot:
    def __init__(self, tocken):
        self.tocken: str = tocken
        self.url: str = f'https://api.telegram.org/bot{tocken}/'
        self.last_update: Int = 0

        self.__text_cmds   = {}
        self.__cmd_cmds    = {}
        self.__stick_cmds  = {}
        self.__global_cmds = {}

        self.__callbacks = {}

        self.__current_chat_id = None

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

        self.__current_chat_id = msg.chat.id

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

            splited_text = lower_text.split(maxsplit=1)[0]
            if splited_text in self.__cmd_cmds:
                cmd: types._CmdOpt = self.__cmd_cmds[splited_text]
                
                if cmd.with_data:
                    cmd.func(msg, cmd.parse(msg.text))
                else:
                    cmd.func(msg)

        if msg.sticker:
            if 'sticker' in self.__global_cmds:
                self.__global_cmds['sticker'](msg)

            if msg.sticker.file_id in self.__stick_cmds:
                self.__stick_cmds[msg.sticker.file_id](msg)

        self.__current_chat_id = None

    def __process_callback(self, json_callback: dict):
        callback = types.CallbackQuery(json_callback)

        self.__current_chat_id = callback.user.id

        if callback.data in self.__callbacks:
            self.__callbacks[callback.data](callback)

        self.__current_chat_id = None


    def send_msg(self, text: str, chat_id: int = None, keyboard = None, remove_reply:bool=False):
        msg_json = {
            'chat_id': chat_id if chat_id else self.__current_chat_id, 
            'text': text, 
        }

        if remove_reply:
            msg_json['reply_markup'] = json.dumps({'remove_keyboard': True})

        elif keyboard:
            msg_json['reply_markup'] = json.dumps(keyboard.to_dict())

        self.__get_method('sendMessage', msg_json)

    def edit_msg_text(self, msg_id: int, text: str, chat_id: int = None, keyboard=None):
        msg_json = {
            'chat_id': chat_id if chat_id else self.__current_chat_id,
            'message_id': msg_id,
            'text': text
        }

        if keyboard:
            msg_json['reply_markup'] = json.dumps(keyboard.to_dict())

        self.__get_method('editMessageText', msg_json)

    def send_sticker(self, stick: str, chat_id: int = None):
            self.__get_method('sendSticker', {
                'chat_id': chat_id if chat_id else self.__current_chat_id, 
                'sticker': stick
            })

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
                self.__text_cmds[text.lower()] = types._TextOpt(func, reg, text)

            if texts:
                for msg in texts:
                    self.__text_cmds[msg.lower()] = types._TextOpt(func, reg, msg)
            
            if cmds:
                for cmd in cmds:
                    cmd_opt = types._CmdOpt(func, cmd)
                    self.__cmd_cmds[cmd_opt.cmd] = cmd_opt

            if stickers:
                for sticker in stickers:
                    self.__stick_cmds[sticker] = func

            if msg_type:
                self.__global_cmds[msg_type] = func

        return decorator

    def on_callback(self, data):
        def decorator(func):
            if type(data) is str:
                self.__callbacks[data] = func
            elif type(data) is list:
                for d in data:
                    self.__callbacks[d] = func

        return decorator

    def run(self):
        try:
            while True:
                updates = self.__wait_updates()

                for update in updates:
                    if 'message' in update:
                        self.__process_message(update['message'])
                    
                    elif 'callback_query' in update:
                        self.__process_callback(update['callback_query'])

                    self.last_update = update['update_id']
        except KeyboardInterrupt:
            quit()