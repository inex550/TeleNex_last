# TeleNex

TeleNex это Python модуль для лёгкого создания Telegram ботов

____

## Использование

```python
from teleNex import Bot

bot = Bot('<tocken>')

@bot.on_message( cmds=['start'] )
def start(msg):
  bot.send_msg('Bot started! :D')
  
bot.run()
```

____

## Установка
```
pip install teleNex
```

____

## Документация
[Про Bot class](#about-bot-class)

[Методы](#методы)
> [send_msg](#send_msg) \
> [send_sticker](#send_sticker) \
> [send_photo](#send_photo) \
> [send_audio](#send_audio)

[Типы](#типы)
> [InlineKeyboard](#inlinekeyboard) \
> [ReplyKeyboard](#replykeyboard)

[Декораторы](#декораторы)
> [@on_message](#on_message) \
> [@on_callback](#on_callback)

### Про Bot клас
Bot это главный класс TeleNex, при помощи него отправляются сообщения и файлы. 
Импортировать его можно так:
```python
from teleNex import Bot
```

Создать объект бота можно так:
```python
bot = Bot('<tocken>')
```
\<tocken\> уникальный индентификатор бота. Можно получить у @BotFather

Чтобы запустить бота, используйте функцию run:
```python
bot.run()
```

### Методы

#### send_msg

Для отправки сообщений используется метод send_msg класса Bot. Например:
```python
bot.send_msg('I am the bot :D')
```

По умолчанию сообщение отправляется в чат, из которого было получено последнее сообщение
Но вы так же можете явно указать id чата, в который хотите отправить сообщение при помощи параметра chat_id:
```python
bot.send_msg('I am the bot :D', chat_id=<chat id>)
```
\<chat id\> - Целочисленное значение - идентификатор чата

Вы так же можете добавить параметр keyboard для отправки клавиатуры:
```python
bot.send_msg('I am the bot :D', keyboard=keyboard_object)
```

Как создать клавиатуру рассказано [здесь](#inlinekeyboard)

Что бы удалить отправленный ReplyKeyboard можно передать в метод параметр remove_reply со значением True:
```python
bot.send_msg('I am the bot :D', remove_reply=True)
```

#### send_sticker

Для отправки стикеров используется метод send_sticker класса Bot. Например:
```python
bot.send_sticker('<sticker_id>')
```
\<sticker_id\> - Строковое значение - идентификатор стикера. Можно получить например у @idstickerbot

Так же этот метод имеет такие же параметры chat_id, keyboard и remove_keyboard, как у [send_msg](#send_msg)

#### send_photo

Для отправки изображений используется метод send_image класса Bot. Например:
```python
bot.send_photo('<photo>')
```

<photo> - file_id изображения или URL на изображение
  
Так же этот метод имеет такие же параметры chat_id, keyboard и remove_keyboard, как у [send_msg](#send_msg)

#### send_audio
Для отправки аудио используется метод send_audio класса Bot. Например:
```python
bot.send_audio('<audio>')
```

<audio> - file_id аудио или URL на аудио
  
Так же этот метод имеет такие же параметры chat_id, keyboard и remove_keyboard, как у [send_msg](#send_msg)

### Типы

Все типы определены в types. types нужно импортировать из teleNex:
```python
from teleNex import types
```
Далее ображение ко всем типам будет производится так: types.<имя типа>
Но вы можете импортировать каждый тип по отдельности и обращатся к ним на прямую

#### InlineKeyboard
InlineKeyboard используется для создания встроенной в сообщение клавиатуры

Для создания клавиатуры используется класс InlineKeyboardMarkup. Для создания отдельных кнопок InlineKeyboardButton:
```python
keyboard = types.InlineKeyboardMarkup([
  [types.InlineKeyboardButton('Button 1'), types.InlineKeyboardButton('Button 2')],
  [types.InlineKeyboardButton('Button 3'), types.InlineKeyboardButton('Button 4')]
])
```

В конструктор класса InlineKeyboardMarkup нужно передать двумерный массив кнопок (экземпляров класса InlineKeyboardButton) \
В конструктор класса InlineKeyboardButton необходимо передать первым параметром тест, который будет отображаться на кнопке и один любой необязательный параметр (так требудет telegram bot api), следовательно кстати в коде выше ошибка, т.к. я не передал в коструктор InlineKeyboardButton дополнительный параметр

InlineKeyboardButton помимо теста может принимать так же **url** или **callback_data** \
**1. url** - Ссылка на сайт, который откроется в браузере при нажатии на кнопку \
**2. callback_data** - Данные, который telegram клиент отправляет боту при нажатии на кнопку. При помощи декоратора [on_callback](#on_callback) (он реагирует на callback data, переданный в его параметры) можно создать обработчик нажатия на кнопку

Исправиленный вариант кода выше:
```python
keyboard = types.InlineKeyboardMarkup([
  [types.InlineKeyboardButton('Button 1', url='telegram.org'), types.InlineKeyboardButton('Button 2', url='telegram.org')],
  [types.InlineKeyboardButton('Button 3', url='telegram.org'), types.InlineKeyboardButton('Button 4', url='telegram.org')]
])
Теперь при нажатии на кнопку пользователь сможет перейти на сайт telegran
```

#### ReplyKeyboard
ReplyKeyboard используется для создания клавиатуры, которая находится у пользователя под полем ввода

Для создания такой клавиатуры используется класс ReplyKeyboardMarkup. Для создания отдельных кнопок KeyboardButton:
```python
keyboard = types.ReplyKeyboardMarkup([
  [types.KeyboardButton('Button 1'), types.KeyboardButton('Button 2')],
  [types.KeyboardButton('Button 3'), types.KeyboardButton('Button 4')]
])
```
В конструктор ReplyKeyboardMarkup нужно передать двумерный массив кнопок (экземпляров класса KeyboardButton) \
В конструктор KeyboardButton необходимо передать только текст, который будет отображаться на кнопке

При нажатии на такую кнопку пользователем будет отправляться сообщение с текстом на кнопке, его можно обработать при помощи декоратора on_message

### Декораторы

#### @on_message

Декоратор on_message используется для обработки пользовательских сообщений. Пример использования:
```python
@bot.on_message(text='Привет, бот')
def hello(msg):
  bot.send_msg('Привет, человек')
```

Параметры декоратора: \
**text** - Текст, при получении которого будет вызываться функция, прикреплённая к декоратору 
```python 
@bot.on_message(text='Привет')
```
**texts** - Список сообщений, при получении которых будет вызываться функция, прикреплённая к декоратору
```python
@bot.on_message(texts=['Привет', 'Хай'])
```
**cmds** - Список команд, при получении которых будет вызываться функция, прикреплённая к декоратору
```python
@bot.on_message(cmds=['start', 'hello'])
```
**stickers** - Список file_id стикеров. При получении стикера с file_id, указанным в списке будет вызываться функция, прикреплённая к декоратору
```python
@bot.on_message(stickers=['CAACAgIAAxkBAAIBKl-S6V4tHIOifJync2dskxwbYFzhAAK2AAPA-wgAAQ8U9O_Fy4sLGwQ'])
```
**msg_type** - Тип сообщения. Как значение можно указать только 'text', 'sticker' или 'all'. Если указано значение 'text', то при получении любого текстового сообщения будет вызываться функция, прикреплённая к декоратору. При значени 'sticker' функция будет вызываться при получении любого стикера. Если же указано значение 'all', функция будет вызываться при получении любого сообщения
```python
@bot.on_message(msg_type='text')
```
**reg** - Если присвоено True, то полученный текст будет обрабатываться вне зависимости от регистра. По умолчанию reg = True
```python
@bot.on_message(text='Привет', reg = True)
``` 
При получении ботом например приВеТ, функция, прикреплённая к декоратору будет вызвана, т.к. reg равен True
```python
@bot.on_message(text='Привет', reg = False)
```
Теперь, при получении ботом сообщения приВеТ функцтя вызвана не будет, она будет вызвана только в случае, если пришло сообщение Привет

Каждая функция, прикреплённая к декоратору on_message должна иметь один параметр. При вызове функции в этот параметр передаётся значение типа [Message](#message) - сообщение пользователя

#### on_callback

Декоратор on_callback может использоваться для обработки нажатий на InlineKeyboardButton. Если в конструкторе InlineKeyboardButton присвоить в параметр callback_data какое-либо строковое значение, то при нажатии на кнопку, это значение будет отправлено боту в виде [CallbackQuery](#callbackquery), который можно поймать и обработать при помощи декоратора on_callback. Пример:
```python
...
keyboard = InlineKeyboardMarkup([
  [InlineKeyboardButton('Click Me', callback_data='clickme')]
])
...
@bot.on_callback('clickme')
def clickMe_clicked(cb):
  bot.send_msg('Вы кликнули на Click Me')
```
В on_callback можно передать как одно значение, так и список

Функция, прикреплённая к on_callback должна иметь один параметр. В этот параметр будет передаваться значение типа [CallbackQuery](#callbackquery) - пришедший callback при нажатии на кнопку
____

## License

[MIT](https://choosealicense.com/licenses/mit/)
