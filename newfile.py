import os
from time import time
from datetime import datetime as dt, timedelta
import asyncio
import cv2
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from telethon import events, TelegramClient
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL
import requests

# تحميل التوكن ومعلومات الاتصال
API_ID = os.getenv("26957529")
API_HASH = os.getenv("ffe7d862b0a31893682a62bbc0654ced")
BOT_TOKEN = os.getenv("6383532072:AAGkOq2B-0gcVwwv8OI6l_N2v13SsaxqqD0")

# إعدادات بوت تليثون
gagan = TelegramClient('gagan', API_ID, API_HASH)
gagan.start(bot_token=BOT_TOKEN)

# دوال المساعدة
def humanbytes(size):
    # تحويل حجم الملف إلى وحدات قابلة للقراءة
    if not size:
        return "0B"
    power = 1024
    t_n = 0
    while size > power:
        size /= power
        t_n += 1
    return f"{round(size, 2)}{['B', 'KB', 'MB', 'GB', 'TB'][t_n]}"

def get_youtube_video_info(url):
    # استخراج معلومات الفيديو من YouTube
    ydl_opts = {'quiet': True, 'skip_download': True}
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        if not info_dict:
            return None
        return {
            'title': info_dict.get('title', 'Unknown Title'),
            'duration': info_dict.get('duration', 0),  # المدة بالثواني
        }

# أوامر البوت
@gagan.on(events.NewMessage(incoming=True, func=lambda e: e.is_private, pattern='/speedtest'))
async def speedtest_command(event):
    # تنفيذ اختبار السرعة
    await event.reply("Running Speed Test. Please wait...")
    try:
        test = Speedtest()
        test.get_best_server()
        test.download()
        test.upload()
        result = test.results.dict()
        # عرض نتائج اختبار السرعة
        speed_text = f'''
        Download Speed: {humanbytes(result['download'])}/s
        Upload Speed: {humanbytes(result['upload'])}/s
        Ping: {result['ping']} ms
        ISP: {result['client']['isp']}
        IP Address: {result['client']['ip']}
        '''
        await event.reply(speed_text)
    except Exception as e:
        await event.reply(f"Speedtest failed: {str(e)}")

@gagan.on(events.NewMessage(incoming=True, func=lambda e: e.is_private, pattern='/stats'))
async def stats_command(event):
    # استعراض إحصائيات النظام
    currentTime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    osUptime = (dt.fromtimestamp(time()) - dt.fromtimestamp(boot_time())).strftime("%H:%M:%S")
    total, used, free, percent = disk_usage('/')
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(net_io_counters().bytes_sent)
    recv = humanbytes(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    swap_t = humanbytes(swap.total)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_t = humanbytes(memory.total)
    mem_a = humanbytes(memory.available)
    mem_u = humanbytes(memory.used)
    stats_text = f'''
    Bot Uptime: {osUptime}
    OS Uptime: {currentTime}
    Total Disk Space: {total}
    Used: {used} | Free: {free}
    Upload: {sent}
    Download: {recv}
    CPU Usage: {cpuUsage}%
    RAM Usage: {mem_p}%
    Physical Cores: {p_core}
    Total Cores: {t_core}
    SWAP Usage: {swap_t} | Used: {swap_p}%
    Memory Total: {mem_t}
    Memory Free: {mem_a}
    Memory Used: {mem_u}
    '''
    await event.reply(stats_text)

@gagan.on(events.NewMessage(incoming=True, func=lambda e: e.is_private, pattern='/help'))
async def help_command(event):
    # عرض رسالة المساعدة
    help_text = """
    Available commands:
    /speedtest - Run a speed test
    /stats - Display system stats
    /help - Show this help message
    """
    await event.reply(help_text)

# بدء تشغيل البوت
gagan.run_until_disconnected()