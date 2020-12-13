import requests
from . import types, errors
import json
from typing import *

class Bot:
    def __init__(self, tocken):
        self.tocken: str = tocken
        self.url: str = f'https://api.telegram.org/bot' + tocken + '/'
        self.last_update: int = 0

        self.__text_cmds: List[types._TextOpt]   = {}
        self.__cmd_cmds: List[types._CmdOpt] = {}
        self.__stick_cmds  = {}
        self.__global_cmds = {}

        self.__callbacks   = {}
        self.__callback_funcs = []

        self.__current_chat_id = None

        self.__last_questions = {}
        self.__on_answers: List[types._AnswerOpt] = {}

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

            if msg.chat.id in self.__last_questions:
                qid = self.__last_questions[msg.chat.id]

                if qid in self.__on_answers:
                    self.__on_answers[qid](msg)
                
                if self.__last_questions[msg.chat.id] == qid:
                    self.__last_questions.pop(msg.chat.id)

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

        for cbfunc, func in self.__callback_funcs:
            if cbfunc(callback): func(callback)

        self.__current_chat_id = None


    def send_msg(self, text: str, chat_id: int = None, keyboard: types._KeyboardMarkupBase = None, remove_reply:bool = False):
        msg_json = {
            'chat_id': chat_id if chat_id else self.__current_chat_id, 
            'text': text, 
        }

        if remove_reply:
            msg_json['reply_markup'] = json.dumps({'remove_keyboard': True})

        elif keyboard:
            msg_json['reply_markup'] = json.dumps(keyboard.to_dict())

        res = self.__get_method('sendMessage', msg_json)
        if not res['ok']:
            err = errors.TextMessageError(res)
            if self.raise_errors: 
                raise err
            elif self.print_errors:
                print(err.description)


    def send_photo(self, photo: str, chat_id=None, caption=None, keyboard: types._KeyboardMarkupBase = None, remove_reply:bool=False):
        msg_json = {
            'chat_id': chat_id if chat_id else self.__current_chat_id,
            'photo': photo
        }

        if caption:
            msg_json['caption'] = caption

        if remove_reply:
            msg_json['reply_markup'] = json.dumps({'remove_keyboard': True})

        elif keyboard:
            msg_json['reply_markup'] = json.dumps(keyboard.to_dict())

        res = self.__get_method('sendPhoto', msg_json)
        if res['ok'] == False:
            err = errors.PhotoError(res)
            if self.raise_errors: 
                raise err
            elif self.print_errors:
                print(err.description)

    
    def send_audio(self, audio: str, chat_id=None, caption=None, keyboard: types._KeyboardMarkupBase = None, remove_reply:bool=False):
        msg_json = {
            'chat_id': chat_id if chat_id else self.__current_chat_id,
            'audio': audio
        }

        if caption:
            msg_json['caption'] = caption

        if remove_reply:
            msg_json['reply_markup'] = json.dumps({'remove_keyboard': True})

        elif keyboard:
            msg_json['reply_markup'] = json.dumps(keyboard.to_dict())

        res = self.__get_method('sendAudio', msg_json)
        if res['ok'] == False:
            err = errors.AudioError(res)
            if self.raise_errors: 
                raise err
            elif self.print_errors:
                print(err.description)


    def send_sticker(self, stick: str, chat_id: int = None, keyboard: types._KeyboardMarkupBase = None, remove_reply:bool=False):
        msg_json = {
            'chat_id': chat_id if chat_id else self.__current_chat_id, 
            'sticker': stick
        }

        if remove_reply:
            msg_json['reply_markup'] = json.dumps({'remove_keyboard': True})

        elif keyboard:
            msg_json['reply_markup'] = json.dumps(keyboard.to_dict())

        res = self.__get_method('sendSticker', msg_json)

        if not res['ok']:
            err = errors.StickerError(res)
            if self.raise_errors: 
                raise err
            elif self.print_errors:
                print(err.description)

    
    def get_answer(self, question: str, qid: str, chat_id: int = None):
        if not qid in self.__on_answers:
            raise errors.AnswerError(qid)
        else:
            chat_id = chat_id if chat_id else self.__current_chat_id

            self.send_msg(question, chat_id)
            self.__last_questions[chat_id] = qid

            #self.__on_answers[qid].chat_ids.append(chat_id)
            #self.__last_questions = qid


    def edit_msg(self, msg_id: int, text: str, chat_id: int = None, keyboard=None):
        msg_json = {
            'chat_id': chat_id if chat_id else self.__current_chat_id,
            'message_id': msg_id,
            'text': text
        }

        if keyboard:
            msg_json['reply_markup'] = json.dumps(keyboard.to_dict())

        res = self.__get_method('editMessageText', msg_json)
        if not res['ok']:
            err = errors.EditMessageError(res)
            if self.raise_errors: 
                raise err
            elif self.print_errors:
                print(err.description)


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

    def on_callback(self, data=None, cbfunc = None):    
        def decorator(func):
            if data is not None:
                if type(data) is str:
                    self.__callbacks[data] = func
                elif type(data) is list:
                    for d in data:
                        self.__callbacks[d] = func
            
            if cbfunc is not None:
                self.__callback_funcs.append( (cbfunc, func) )

        return decorator


    def on_answer(self, qid: str):
        def decorator(func):
            self.__on_answers[qid] = func

        return decorator


    def run(self, raise_errors=True, print_errors=False):
        self.raise_errors: bool = raise_errors
        self.print_errors: bool = print_errors
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