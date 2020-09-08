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
        self.lang_code: str  = json_from.get('languege_code')
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
        self.file_id: str = json_stick.get('file_id')
        self.file_unique_id: str = json_stick.get('file_unique_id')
        self.width: int = json_stick.get('width')
        self.height: int = json_stick.get('height')
        self.is_animated: bool = json_stick.get('is_animated')
        self.file_size: int = json_stick.get('file_size')
        self.set_name: Int = json_stick.get('set_name')

class _TextCmdOpt():
    def __init__(self, func, reg: bool, orig: str):
        self.func = func
        self.reg = reg
        self.orig = orig

    def check(self, text: str) -> bool:
        if reg:
            return text.lower() == self.orig.lower()
        else:
            return text == self.orig