class Message:
    def __init__(self, json_msg: dict):
        self.id: int    = json_msg.get('message_id')
        self.text: str  = json_msg.get('text')
        self.date: int  = json_msg.get('date')
        self.chat: Chat = Chat(json_msg.get('chat'))
        self.user: User = None
        self.sticker: Sticker = None
        
        if 'from' in json_msg:
            self.user = User(json_msg.get('from'))

        if 'sticker' in json_msg:
            self.sticker = Sticker(json_msg.get('sticker'))

class User:
    def __init__(self, json_from: dict):
        self.id: int         = json_from.get('id')
        self.first_name: str = json_from.get('first_name')
        self.last_name: str  = json_from.get('last_name')
        self.is_bot: bool    = json_from.get('is_bot')
        self.lang_code: str  = json_from.get('language_code')
        self.username: str   = json_from.get('username')

class Chat:
    def __init__(self, json_chat: dict):
        self.id: int         = json_chat.get('id')
        self.first_name: str = json_chat.get('first_name')
        self.last_name: str  = json_chat.get('last_name')
        self.type: str       = json_chat.get('private')
        self.username: str   = json_chat.get('username')

class Sticker:
    def __init__(self, json_stick: dict):
        self.file_id: str        = json_stick.get('file_id')
        self.file_unique_id: str = json_stick.get('file_unique_id')
        self.width: int          = json_stick.get('width')
        self.height: int         = json_stick.get('height')
        self.is_animated: bool   = json_stick.get('is_animated')
        self.file_size: int      = json_stick.get('file_size')
        self.set_name: Int       = json_stick.get('set_name')

class _KeyboardMarkupBase:
    def __init__(self, keyboard: list = None):
        if keyboard:
            self.keyboard = keyboard
        else:
            self.keyboard = [[]]

    def item(self, line, el):
        return self.keyboard[line][el]
    
    def line(self, line):
        return self.keyboard[line]

    def add_line(self, btns_line: list = None):
        if btns_line:
            self.keyboard.append(btns_line)
        else:
            self.keyboard.append([])

    def add_btn(self, btn, line = -1):
        self.keyboard[line].append(btn)

class ReplyKeyboardMarkup(_KeyboardMarkupBase):
    def __init__(self, keyboard: list= None, resize_keyboard: bool = False, one_time_keyboard: bool = False):
        super().__init__(keyboard)
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard

    def to_dict(self):
        keyboard_json = [ [ btn.to_dict() for btn in btns_line ] for btns_line in self.keyboard ]

        return {
            'keyboard': keyboard_json,
            'resize_keyboard': self.resize_keyboard,
            'one_time_keyboard': self.one_time_keyboard
        }

class InlineKeyboardMarkup(_KeyboardMarkupBase):
    def __init__(self, keyboard: list = None):
        super().__init__(keyboard)

    def to_dict(self):
        return {
            'inline_keyboard': [[btn.to_dict() for btn in btns_line] for btns_line in self.keyboard]
        }

class KeyboardButton:
    def __init__(self, text: str):
        self.text = text

    def to_dict(self):
        return {
            'text': self.text
        }

class InlineKeyboardButton:
    def __init__(self, text: str, url: str=None, callback_data=None):
        self.text: str = text
        self.url: str = url
        self.callback_data = callback_data

    def to_dict(self):
        btn_dict = { 'text': self.text }

        if self.url:
            btn_dict['url'] = self.url

        if self.callback_data:
            btn_dict['callback_data'] = self.callback_data

        return btn_dict

class CallbackQuery:
    def __init__(self, json_callback: dict):
        self.id: str = json_callback.get('id')
        self.user: User = User(json_callback['from'])
        self.data: str = json_callback.get('data')

        if 'message' in json_callback:
            self.message = Message(json_callback['message'])

class _TextOpt:
    def __init__(self, func, reg: bool, orig: str):
        self.func = func
        self.reg = reg
        self.orig = orig

    def check(self, text: str) -> bool:
        if reg:
            return text.lower() == self.orig.lower()
        else:
            return text == self.orig

class _CmdOpt:
    def __init__(self, func, cmd: str):
        self.func = func

        self.with_data: bool = cmd[-1] == '~'
        self.cmd = '/' + ( cmd[0:-1] if self.with_data else cmd ).lower()

    def parse(self, cmd_line: str):
            temp = cmd_line.split(maxsplit=1)

            if len(temp) == 2:
                return temp[1]
            
            return None