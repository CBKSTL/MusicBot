import discord
import os
import asyncio
import re
import requests
import config
from discord import app_commands
from discord.ext import commands, tasks
from youtube_search import YoutubeSearch
from pytube import YouTube
from PIL import Image
from io import BytesIO

def clean_filename(filename):
    cleaned_filename = re.sub(r'[\\/:"*?<>|]', '_', filename)
    return cleaned_filename

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="music"))
    print("Bot запущен.")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Ошибка синхронизации команд: {e}")

class GuildMusicPlayer:
    def __init__(self, voice_client, yt, stream):
        self.voice_client = voice_client
        self.yt = yt
        self.stream = stream
        self.ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -af aresample=async=1'
        }
        self.loop = False
        self.message = None  # Храним сообщение с кнопками
        self.update_view_task = None  # Задача для обновления кнопок

    def play(self):
        self.voice_client.play(discord.FFmpegPCMAudio(self.stream.url, **self.ffmpeg_options), after=lambda e: asyncio.run_coroutine_threadsafe(self.after_playback(), bot.loop))

    async def after_playback(self):
        if self.loop:
            self.play()
        else:
            if self.voice_client:
                await self.voice_client.disconnect()
            if self.message:
                await self.message.edit(view=None)  # Отключаем кнопки после завершения воспроизведения
            if self.update_view_task:
                self.update_view_task.cancel()  # Останавливаем обновление кнопок

    async def update_view(self):
        while True:
            if self.message:
                await self.message.edit(view=MusicView(self))  # Обновляем сообщение с кнопками
            await asyncio.sleep(150)  # Ждем 10 минут
            print("Кнопка re-1")

class MusicView(discord.ui.View):
    def __init__(self, player):
        super().__init__()
        self.player = player

    @discord.ui.button(emoji="🔁", style=discord.ButtonStyle.blurple)
    async def repeat(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.player.loop = not self.player.loop
        await interaction.response.defer()
        await interaction.followup.send(f"Режим повтора {'включен' if self.player.loop else 'выключен'}.", ephemeral=True)

    @discord.ui.button(emoji="⏸️", style=discord.ButtonStyle.blurple)
    async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.player.voice_client.is_playing():
            self.player.voice_client.pause()
        await interaction.response.defer()

    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.blurple)
    async def resume(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.player.voice_client.is_paused():
            self.player.voice_client.resume()
        await interaction.response.defer()

    @discord.ui.button(emoji="⛔", style=discord.ButtonStyle.grey)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_state = interaction.guild.get_member(interaction.user.id).voice
        if voice_state is None or voice_state.channel is None:
            await interaction.response.send_message("Вы должны быть в голосовом канале, чтобы использовать эту команду.")
            return
        await interaction.response.defer()

        try:
            voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
            if voice_client and voice_client.is_playing():
                voice_client.stop()
                await interaction.followup.send("Воспроизведение музыки остановлено.", ephemeral=True)
                await voice_client.disconnect()
            else:
                await interaction.followup.send("В данный момент ничего не воспроизводится.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f'Произошла ошибка: {e}', ephemeral=True)

def resize_image(image_url, output_filename, max_height):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Получаем исходные размеры изображения
    width, height = img.size

    # Рассчитываем новое соотношение сторон и новую ширину
    aspect_ratio = width / height
    new_height = max_height
    new_width = int(aspect_ratio * new_height)

    # Изменяем размер изображения, сохраняя пропорции
    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Сохраняем уменьшенное изображение
    img.save(output_filename)

@bot.tree.command(name="play", description='Поиск и воспроизведение музыки в гс канале')
@app_commands.describe(запрос="Поиск и воспроизведение музыки в гс канале")
async def play_music(interaction: discord.Interaction, запрос: str):
    voice_state = interaction.guild.get_member(interaction.user.id).voice
    if voice_state is None or voice_state.channel is None:
        await interaction.response.send_message("Вы должны быть в голосовом канале, чтобы использовать эту команду.")
        return

    await interaction.response.defer()

    voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()

    try:
        voice_client = await voice_state.channel.connect()

        if запрос.startswith("http"):
            video_url = запрос
        else:
            results = YoutubeSearch(запрос, max_results=1).to_dict()
            if not results:
                await interaction.followup.send("По вашему запросу ничего не найдено.")
                return
            video_url = "https://www.youtube.com" + results[0]['url_suffix']

        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()

        # Создание встроенного сообщения (embed)
        spacer = '--' * 34
        embed = discord.Embed(title=yt.title, description=f"Длительность: {yt.length // 60}:{yt.length % 60:02d}\n{spacer}", color=0x1E90FF)
        embed.set_footer(text=f"added by {interaction.user.display_name}")
        embed.set_thumbnail(url=yt.thumbnail_url)  # Устанавливаем URL превью-изображения

        player = GuildMusicPlayer(voice_client, yt, stream)
        player.play()

        # Отправляем сообщение с кнопками и сохраняем его в player
        player.message = await interaction.followup.send(embed=embed, view=MusicView(player))

        # Запускаем задачу для обновления кнопок
        player.update_view_task = asyncio.create_task(player.update_view())
        
    except Exception as e:
        await interaction.followup.send(f'Произошла ошибка: {e}', ephemeral=True)

@bot.tree.command(name="stop", description='Остановить воспроизведение музыки и очистить очередь')
async def stop_playing(interaction: discord.Interaction):
    voice_state = interaction.guild.get_member(interaction.user.id).voice
    if voice_state is None or voice_state.channel is None:
        await interaction.response.send_message("Вы должны быть в голосовом канале, чтобы использовать эту команду.")
        return
    await interaction.response.defer()

    try:
        voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.followup.send("Воспроизведение музыки остановлено.", ephemeral=True)
            await voice_client.disconnect()
        else:
            await interaction.followup.send("В данный момент ничего не воспроизводится.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f'Произошла ошибка: {e}', ephemeral=True)

bot.run(config.token)
