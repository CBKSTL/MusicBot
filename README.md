# MusicBot / Музыкальный Бот 🎶

[English version below]

## Описание
MusicBot — это Discord-бот, который позволяет воспроизводить музыку из YouTube в голосовых каналах сервера. Он поддерживает команды для поиска, воспроизведения, паузы и остановки музыки.

## Установка

### Шаг 1: Установка Python 3.10.6
1. Скачайте установщик Python 3.10.6 с [официального сайта Python](https://www.python.org/downloads/release/python-3106/).
2. Запустите установщик.
3. Обязательно отметьте галочку "Add Python to PATH" внизу окна установщика.
4. Нажмите "Install Now".

### Шаг 2: Установка библиотек
1. Откройте cmd Windows
2. Пропишите:
```bash
pip install discord.py asyncio youtube-search-python pytube pillow requests pynacl
```
3. Нажмите Enter

### Шаг 3: Установка FFmpeg
1. Скачайте последнюю сборку FFmpeg с [официального сайта](https://ffmpeg.org/download.html).
2. Распакуйте архив в удобное место, например, C:\ffmpeg.
3. Добавьте путь к папке bin в системную переменную PATH:
    - Откройте "Панель управления" > "Система" > "Дополнительные параметры системы" > "Переменные среды".
    - Найдите переменную Path, нажмите "Изменить".
    - Добавьте новый путь: C:\ffmpeg\bin.

### Шаг 4: Создание файла config.py
Создайте файл `config.py` в той же папке, где находится ваш бот, и добавьте туда ваш токен:
```python
# config.py
token = 'ВАШ_API_ТОКЕН_ЗДЕСЬ'
```

## Использование
1. Запустите бота командой:
```bash
python main.py
```
2. Подключитесь к голосовому каналу на вашем сервере Discord.
3. Используйте команды для управления музыкой.

## Команды
- `!play <запрос>` - Поиск и воспроизведение музыки по запросу.
- `!stop` - Остановить воспроизведение музыки и отключить бота.
- Кнопка 🔁 - Включить/выключить режим повтора.
- Кнопка ⏸️ - Поставить воспроизведение на паузу.
- Кнопка ▶️ - Возобновить воспроизведение.
- Кнопка ⛔ - Остановить воспроизведение и отключить бота.

## English

### Description
MusicBot is a Discord bot that allows you to play music from YouTube in your server's voice channels. It supports commands for searching, playing, pausing, and stopping music.

### Installation

#### Step 1: Install Python 3.10.6
1. Download the Python 3.10.6 installer from the [official Python website](https://www.python.org/downloads/release/python-3106/).
2. Run the installer.
3. Make sure to check the box "Add Python to PATH" at the bottom of the installer window.
4. Click "Install Now".

#### Step 2: Install Libraries
1. Open the Windows cmd
2. Run the following command:
```bash
pip install discord.py asyncio youtube-search-python pytube pillow requests pynacl
```
3. Press Enter

#### Step 3: Install FFmpeg
1. Download the latest build of FFmpeg from the [official website](https://ffmpeg.org/download.html).
2. Unzip the archive to a convenient location, such as C:\ffmpeg.
3. Add the path to the bin folder to the system PATH variable:
    - Open "Control Panel" > "System" > "Advanced system settings" > "Environment Variables".
    - Find the Path variable and click "Edit".
    - Add a new path: C:\ffmpeg\bin.

#### Step 4: Create config.py file
Create a `config.py` file in the same folder as your bot and add your token:
```python
# config.py
token = 'YOUR_API_TOKEN_HERE'
```

### Usage
1. Run the bot with the command:
```bash
python main.py
```
2. Connect to a voice channel on your Discord server.
3. Use the commands to control the music.

### Commands
- `!play <query>` - Search and play music based on the query.
- `!stop` - Stop the music and disconnect the bot.
- Button 🔁 - Toggle repeat mode.
- Button ⏸️ - Pause the music.
- Button ▶️ - Resume the music.
- Button ⛔ - Stop the music and disconnect the bot.

## License
This project is licensed under the MIT License.
