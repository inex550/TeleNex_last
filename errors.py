class _TelegramError(Exception):
    def __init__(self, json_error: dict):
        self.error_code = json_error['error_code']
        self.description = json_error['description']
        super().__init__(self.description)

class AudioError(_TelegramError):
    pass

class PhotoError(_TelegramError):
    pass

class TextMessageError(_TelegramError):
    pass

class StickerError(_TelegramError):
    pass

class EditMessageError(_TelegramError):
    pass