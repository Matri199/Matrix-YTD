#!/usr/bin/env python3

import os
import sys
import re
import subprocess
from urllib.parse import urlparse, parse_qs
from colorama import init, Fore, Style, Back
import platform
import time
from tqdm import tqdm

init(autoreset=True)

DOWNLOAD_DIR = "/sdcard/MATRIX YTD/"
TERMUX_SETUP_DONE = False

def check_dependencies():
    """Check and install required dependencies"""
    required = {
        'colorama': 'pip install colorama --user',
        'yt_dlp': 'pip3 install yt_dlp --user',
        'ffmpeg': 'pkg install ffmpeg -y',
        'tqdm': 'pip install tqdm --user',
        'termux-api': 'pkg install termux-api -y',
        'mutagen': 'pip install mutagen --user',
        'pydub': 'pip install pydub --user'
    }
    print(f"\n{Fore.YELLOW}🔍 Checking dependencies...{Style.RESET_ALL}")
    for dep, cmd in required.items():
        try:
            __import__(dep)
            print(f"{Fore.GREEN}✓ {dep} is installed{Style.RESET_ALL}")
        except ImportError:
            print(f"{Fore.RED}✗ {dep} not found. Installing...{Style.RESET_ALL}")
            try:
                if platform.system() == 'Linux' and 'ANDROID_ROOT' in os.environ:
                    print(f"{Fore.CYAN}Running: {cmd}{Style.RESET_ALL}")
                    os.system(cmd)
                else:
                    print(f"{Fore.YELLOW}⚠ Please install {dep} manually: {cmd}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}❌ Failed to install {dep}: {str(e)}{Style.RESET_ALL}")
    global TERMUX_SETUP_DONE
    if not TERMUX_SETUP_DONE and platform.system() == 'Linux' and 'ANDROID_ROOT' in os.environ:
        print(f"{Fore.CYAN}\nSetting up Termux storage...{Style.RESET_ALL}")
        os.system('yes | termux-setup-storage > /dev/null 2>&1')
        TERMUX_SETUP_DONE = True

def print_banner():
    os.system('clear')
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    banner = f"""
{colors[0]}╔══════════════════════════════════════════════════════╗
{colors[1]}║ ███╗ ███╗██╗ ██╗███████╗██╗ ██████╗███████╗ ║
{colors[2]}║ ████╗ ████║██║ ██║██╔════╝██║██╔════╝██╔════╝ ║
{colors[3]}║ ██╔████╔██║██║ ██║███████╗██║██║ █████╗ ║
{colors[4]}║ ██║╚██╔╝██║██║ ██║╚════██║██║██║ ██╔══╝ ║
{colors[5]}║ ██║ ╚═╝ ██║╚██████╔╝███████║██║╚██████╗███████╗ ║
{colors[0]}║ ═══════════════════════════════════════════════════ ║
{colors[1]}║ 🎵 M U S I C 🎵 ║
{colors[2]}║ ─────────────────────────────────────────────────── ║
{colors[3]}║ 🚀 MATRIX - DOWNLOADER 🚀 ║
{colors[4]}║ ═══════════════════════════════════════════════════ ║
{colors[5]}║ 📢 Telegram: https://t.me/MatriXXXXXXXXX ║
{colors[0]}║ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ║
{colors[1]}╚══════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80
    centered_banner = "\n".join(line.center(terminal_width) for line in banner.split("\n"))
    for line in centered_banner.split('\n'):
        for char in line:
            print(char, end='', flush=True)
            time.sleep(0.002)
        print()
    time.sleep(0.5)
    os.system('clear')
    print(banner)
    time.sleep(0.5)

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def rename_file_prompt(default_name):
    print(f"\n{Fore.CYAN}📝 Suggested filename: {Fore.LIGHTYELLOW_EX}{default_name}{Style.RESET_ALL}")
    rename = input(f"{Fore.LIGHTBLUE_EX}✏ Rename file? (y/n): {Style.RESET_ALL}").lower()
    if rename == 'y':
        new_name = input(f"{Fore.CYAN}Enter new filename (without extension): {Style.RESET_ALL}").strip()
        if new_name:
            ext = os.path.splitext(default_name)[1]
            return f"{new_name}{ext}"
    return default_name

def get_video_info(url):
    import yt_dlp
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        print(f"\n{Fore.LIGHTRED_EX}🔥 {Fore.RED}✖ Error getting video info: {str(e)}{Style.RESET_ALL}")
        return None

def convert_webm_to_mp3(input_file, output_file=None):
    if not os.path.exists(input_file):
        print(f"{Fore.RED}❌ Error: File {input_file} not found!{Style.RESET_ALL}")
        return False
    default_name = os.path.splitext(os.path.basename(input_file))[0] + ".mp3"
    output_file = output_file or os.path.join(DOWNLOAD_DIR, default_name)
    final_name = rename_file_prompt(os.path.basename(output_file))
    output_file = os.path.join(DOWNLOAD_DIR, final_name)
    try:
        with tqdm(total=100, desc=f"{Fore.BLUE}Converting to MP3{Style.RESET_ALL}",
                  bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.CYAN, Fore.RESET)) as pbar:
            command = [
                'ffmpeg', '-y', '-i', input_file,
                '-q:a', '2', '-vn', output_file
            ]
            process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       universal_newlines=True)
            for i in range(100):
                time.sleep(0.03)
                pbar.update(1)
                if process.poll() is not None:
                    break
            process.wait()
        if process.returncode == 0:
            print(f"{Fore.GREEN}✅ Conversion successful! File saved to:\n{output_file}{Style.RESET_ALL}")
            return output_file
        else:
            raise subprocess.CalledProcessError(process.returncode, command)
    except Exception as e:
        print(f"{Fore.RED}❌ Conversion failed: {str(e)}{Style.RESET_ALL}")
        return False

def play_audio(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.RED}❌ Error: File not found!{Style.RESET_ALL}")
            return False
        print(f"\n{Fore.MAGENTA}🎧 Preparing to play: {Fore.CYAN}{os.path.basename(file_path)}{Style.RESET_ALL}")
        methods = [
            lambda: subprocess.run(['termux-media-player', 'play', file_path], check=True),
            lambda: subprocess.run(['termux-media-player', 'play', file_path, '-l'], check=True),
            lambda: subprocess.run(['play-audio', file_path], check=True),
            lambda: subprocess.run(['ffplay', '-nodisp', '-autoexit', file_path], check=True)
        ]
        success = False
        for method in methods:
            try:
                method()
                success = True
                break
            except:
                continue
        if not success:
            raise RuntimeError("All playback methods failed")
        print(f"{Fore.GREEN}▶ Now playing... (Press Ctrl+C to stop){Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}⏯ Controls: {Style.RESET_ALL}")
        print(f"{Fore.CYAN}[P] {Fore.WHITE}Pause/Resume")
        print(f"{Fore.CYAN}[S] {Fore.WHITE}Stop")
        print(f"{Fore.CYAN}[Q] {Fore.WHITE}Quit player")
        while True:
            try:
                key = input().lower()
                if key == 'p':
                    subprocess.run(['termux-media-player', 'pause'])
                elif key == 's':
                    subprocess.run(['termux-media-player', 'stop'])
                    break
                elif key == 'q':
                    subprocess.run(['termux-media-player', 'stop'])
                    return True
            except KeyboardInterrupt:
                subprocess.run(['termux-media-player', 'stop'])
                print(f"\n{Fore.YELLOW}⏹ Playback stopped{Style.RESET_ALL}")
                break
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Playback error: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚠ Make sure you have Termux:API installed and permissions granted{Style.RESET_ALL}")
        return False

def download_video(url, quality='best'):
    import yt_dlp
    try:
        video_info = get_video_info(url)
        if not video_info:
            return None
        is_audio = quality == 'bestaudio/best'
        ext = 'mp3' if is_audio else 'mp4'
        default_title = sanitize_filename(video_info['title'])
        default_filename = f"{default_title}.{ext}"
        output_template = os.path.join(DOWNLOAD_DIR, f"{default_title}.%(ext)s")
        ydl_opts = {
            'format': quality,
            'outtmpl': output_template,
            'progress_hooks': [progress_hook],
            'quiet': True,
            'no_warnings': True,
            'postprocessors': []
        }
        if is_audio:
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            })
        else:
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            })
        print(f"\n{Fore.GREEN}📡 Downloading: {Fore.LIGHTYELLOW_EX}{default_title}{Style.RESET_ALL}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)
            downloaded_file = os.path.splitext(downloaded_file)[0] + ('.mp3' if is_audio else '.mp4')
        final_filename = rename_file_prompt(os.path.basename(downloaded_file))
        final_path = os.path.join(DOWNLOAD_DIR, final_filename)
        if final_filename != os.path.basename(downloaded_file):
            os.rename(downloaded_file, final_path)
            downloaded_file = final_path
        print(f"\n{Fore.LIGHTGREEN_EX}🎉 Download completed!{Style.RESET_ALL}")
        print(f"{Fore.LIGHTCYAN_EX}📂 Saved to: {Fore.LIGHTYELLOW_EX}{downloaded_file}{Style.RESET_ALL}")
        return downloaded_file
    except Exception as e:
        print(f"\n{Fore.RED}❌ Download Error: {str(e)}{Style.RESET_ALL}")
        return None

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A').strip()
        speed = d.get('_speed_str', 'N/A').strip()
        eta = d.get('_eta_str', 'N/A').strip()
        icons = ['◐', '◓', '◑', '◒']
        spinner = icons[int(time.time() * 4) % len(icons)]
        try:
            pct_num = float(percent.replace('%',''))
            if pct_num < 30:
                color = Fore.RED
            elif pct_num < 70:
                color = Fore.YELLOW
            else:
                color = Fore.GREEN
        except:
            color = Fore.CYAN
        progress_bar = f"{spinner} {color}{percent:>6} {Fore.MAGENTA}■ {speed:>10} {Fore.BLUE}■ ETA: {eta}"
        print(f"\r{progress_bar}", end='', flush=True)
    elif d['status'] == 'finished':
        print(f"\r{Fore.GREEN}✓ Done!{' '*50}{Style.RESET_ALL}")

def print_menu():
    menu = f"""
{Fore.LIGHTMAGENTA_EX}╔══════════════════════════════════════════════╗
{Fore.LIGHTMAGENTA_EX}║ {Fore.LIGHTCYAN_EX}🎧 M U S I C M E N U 🎧 {Fore.LIGHTMAGENTA_EX}║
{Fore.LIGHTMAGENTA_EX}╠══════════════════════════════════════════════╣
{Fore.LIGHTMAGENTA_EX}║ {Fore.LIGHTGREEN_EX}1. {Fore.LIGHTCYAN_EX}🎥 Download HD Video (YouTube) {Fore.LIGHTMAGENTA_EX}║
{Fore.LIGHTMAGENTA_EX}║ {Fore.LIGHTGREEN_EX}2. {Fore.LIGHTCYAN_EX}🎬 Download 1080p Video (YouTube) {Fore.LIGHTMAGENTA_EX}║
{Fore.LIGHTMAGENTA_EX}║ {Fore.LIGHTGREEN_EX}3. {Fore.LIGHTCYAN_EX}📽 Download 720p Video (YouTube) {Fore.LIGHTMAGENTA_EX}║
{Fore.LIGHTMAGENTA_EX}║ {Fore.LIGHTGREEN_EX}4. {Fore.LIGHTCYAN_EX}🎶 Download High Quality MP3 (YouTube) {Fore.LIGHTMAGENTA_EX}║
{Fore.LIGHTMAGENTA_EX}║ {Fore.LIGHTGREEN_EX}5. {Fore.LIGHTCYAN_EX}🔀 Convert WebM to MP3 {Fore.LIGHTMAGENTA_EX}║
{Fore.LIGHTMAGENTA_EX}║ {Fore.LIGHTGREEN_EX}6. {Fore.LIGHTCYAN_EX}🎵 Play Audio Track {Fore.LIGHTMAGENTA_EX}║
{Fore.LIGHTMAGENTA_EX}║ {Fore.LIGHTGREEN_EX}7. {Fore.LIGHTCYAN_EX}🎵 Download TikTok Video {Fore.LIGHTMAGENTA_EX}║
{Fore.LIGHTMAGENTA_EX}║ {Fore.LIGHTGREEN_EX}8. {Fore.LIGHTCYAN_EX}🎞 Download Instagram Video {Fore.LIGHTMAGENTA_EX}║
{Fore.LIGHTMAGENTA_EX}║ {Fore.LIGHTGREEN_EX}9. {Fore.LIGHTCYAN_EX}🐦 Download Twitter Video {Fore.LIGHTMAGENTA_EX}║
{Fore.LIGHTMAGENTA_EX}║ {Fore.LIGHTGREEN_EX}10. {Fore.LIGHTCYAN_EX}📘 Download Facebook Video {Fore.LIGHTMAGENTA_EX}║
{Fore.LIGHTMAGENTA_EX}║ {Fore.LIGHTGREEN_EX}0. {Fore.LIGHTRED_EX}🚪 Exit Program {Fore.LIGHTMAGENTA_EX}║
{Fore.LIGHTMAGENTA_EX}╚══════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(menu)

def get_quality_choice(choice):
    quality_map = {
        '1': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '2': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
        '3': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
        '4': 'bestaudio/best'
    }
    return quality_map.get(choice, 'best')

def extract_youtube_url(text):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    match = re.match(youtube_regex, text)
    if match and match.group(6):
        return f"https://www.youtube.com/watch?v={match.group(6)}"
    return None

def is_tiktok_url(url):
    return 'tiktok.com' in url.lower()

def is_instagram_url(url):
    return 'instagram.com' in url.lower()

def is_twitter_url(url):
    return 'twitter.com' in url.lower() or 'x.com' in url.lower()

def is_facebook_url(url):
    return 'facebook.com' in url.lower() or 'fb.watch' in url.lower()

def main():
    check_dependencies()
    print_banner()
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    while True:
        print_menu()
        choice = input(f"\n{Fore.MAGENTA}✨ {Fore.LIGHTCYAN_EX}Enter your choice [0-10]: {Style.RESET_ALL}").strip()
        if choice == '0':
            print(f"\n{Fore.LIGHTMAGENTA_EX}🎵 Thank you for using MUSIC Downloader!{Style.RESET_ALL}")
            print(f"{Fore.LIGHTBLUE_EX}🌟 All downloads are saved in: {Fore.LIGHTYELLOW_EX}{DOWNLOAD_DIR}{Style.RESET_ALL}\n")
            break
        if choice not in [str(i) for i in range(0, 11)]:
            print(f"{Fore.RED}⚠ Invalid choice. Please try again.{Style.RESET_ALL}")
            continue
        if choice == '5':
            input_file = input(f"\n{Fore.CYAN}🌐 Enter path to WebM file: {Style.RESET_ALL}").strip()
            if not os.path.exists(input_file):
                print(f"{Fore.RED}❌ File not found!{Style.RESET_ALL}")
                continue
            output_file = convert_webm_to_mp3(input_file)
            if output_file:
                play_choice = input(f"\n{Fore.LIGHTBLUE_EX}🎧 Play the converted file now? {Fore.LIGHTCYAN_EX}(y/n): {Style.RESET_ALL}").lower()
                if play_choice == 'y':
                    play_audio(output_file)
            continue
        if choice == '6':
            audio_file = input(f"\n{Fore.CYAN}🎵 Enter path to audio file: {Style.RESET_ALL}").strip()
            play_audio(audio_file)
            continue
        if choice == '7':
            tiktok_url = input(f"\n{Fore.CYAN}🌐 Enter TikTok video URL: {Style.RESET_ALL}").strip()
            if not is_tiktok_url(tiktok_url):
                print(f"{Fore.RED}❌ Invalid TikTok URL!{Style.RESET_ALL}")
                continue
            print(f"\n{Fore.LIGHTGREEN_EX}⚡ Downloading TikTok video...{Style.RESET_ALL}")
            downloaded_file = download_video(tiktok_url, quality='best')
            if downloaded_file:
                print(f"{Fore.LIGHTGREEN_EX}🎉 TikTok download complete!{Style.RESET_ALL}")
            continue
        if choice == '8':
            insta_url = input(f"\n{Fore.CYAN}🌐 Enter Instagram video URL: {Style.RESET_ALL}").strip()
            if not is_instagram_url(insta_url):
                print(f"{Fore.RED}❌ Invalid Instagram URL!{Style.RESET_ALL}")
                continue
            print(f"\n{Fore.LIGHTGREEN_EX}⚡ Downloading Instagram video...{Style.RESET_ALL}")
            downloaded_file = download_video(insta_url, quality='best')
            if downloaded_file:
                print(f"{Fore.LIGHTGREEN_EX}🎉 Instagram download complete!{Style.RESET_ALL}")
            continue
        if choice == '9':
            twitter_url = input(f"\n{Fore.CYAN}🌐 Enter Twitter/X video URL: {Style.RESET_ALL}").strip()
            if not is_twitter_url(twitter_url):
                print(f"{Fore.RED}❌ Invalid Twitter/X URL!{Style.RESET_ALL}")
                continue
            print(f"\n{Fore.LIGHTGREEN_EX}⚡ Downloading Twitter/X video...{Style.RESET_ALL}")
            downloaded_file = download_video(twitter_url, quality='best')
            if downloaded_file:
                print(f"{Fore.LIGHTGREEN_EX}🎉 Twitter/X download complete!{Style.RESET_ALL}")
            continue
        if choice == '10':
            fb_url = input(f"\n{Fore.CYAN}🌐 Enter Facebook video URL: {Style.RESET_ALL}").strip()
            if not is_facebook_url(fb_url):
                print(f"{Fore.RED}❌ Invalid Facebook URL!{Style.RESET_ALL}")
                continue
            print(f"\n{Fore.LIGHTGREEN_EX}⚡ Downloading Facebook video...{Style.RESET_ALL}")
            downloaded_file = download_video(fb_url, quality='best')
            if downloaded_file:
                print(f"{Fore.LIGHTGREEN_EX}🎉 Facebook download complete!{Style.RESET_ALL}")
            continue
        # YouTube logic
        quality = get_quality_choice(choice)
        url = input(f"\n{Fore.CYAN}🌐 Enter YouTube URL or video ID: {Style.RESET_ALL}").strip()
        if not url.startswith('http') and len(url) == 11 and url.isalnum():
            url = f"https://www.youtube.com/watch?v={url}"
        elif not url.startswith('http'):
            extracted_url = extract_youtube_url(url)
            if extracted_url:
                url = extracted_url
                print(f"{Fore.LIGHTGREEN_EX}🔗 Extracted URL: {Fore.LIGHTCYAN_EX}{url}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Invalid YouTube URL or video ID{Style.RESET_ALL}")
                continue
        print(f"\n{Fore.LIGHTGREEN_EX}⚡ Selected quality: {Fore.LIGHTCYAN_EX}{'MP3 Audio' if choice == '4' else quality.split('+')[0].split('[')[0]}{Style.RESET_ALL}")
        downloaded_file = download_video(url, quality)
        if downloaded_file and choice == '4':
            play_choice = input(f"\n{Fore.LIGHTBLUE_EX}🎧 Play the downloaded audio now? {Fore.LIGHTCYAN_EX}(y/n): {Style.RESET_ALL}").lower()
            if play_choice == 'y':
                play_audio(downloaded_file)

if __name__ == "__main__":
    main()
