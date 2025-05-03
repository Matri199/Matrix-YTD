# MATRIX-YTD

A powerful, interactive music and video downloader for YouTube, TikTok, Instagram, Twitter, and Facebook with a beautiful terminal interface.  
Built for Termux (Android) and Linux, with features like MP3 conversion, playlist support, and more!

---

## ✨ Features

- Download from:
  - **YouTube** (videos, playlists, audio)
  - **TikTok** (public videos)
  - **Instagram** (reels, posts, stories)
  - **Twitter/X** (public videos)
  - **Facebook** (public videos)
- Convert WebM to MP3
- Play downloaded audio (in Termux)
- Colorful, animated terminal interface
- Automatic dependency installation
- Works on Android (Termux) and Linux

---

## 🚀 Installation

1. **Install Termux** (if on Android):  
   [Get Termux from F-Droid](https://f-droid.org/packages/com.termux/)

2. **Clone this repository:**

git clone https://github.com/Matri199/Matrix-YTD.git

cd Matrix-YTD


3. **Run the script:**

python matrix.py

> The script will check and install all dependencies automatically.

---

## 🕹️ Usage

1. **Choose a download option** from the menu (YouTube HD, 1080p, 720p, MP3, TikTok, Instagram, Twitter, Facebook, etc.).
2. **Paste your link or video ID** when prompted.
3. **Follow the prompts** to save or play your download.

**Downloads are saved to:**  
`/sdcard/TRON MUSIC DOWNLOAD/` (on Android/Termux)

---

## 📋 Supported Sites

| Platform    | Supported? | Notes                                         |
|-------------|------------|-----------------------------------------------|
| YouTube     | ✅         | Videos, playlists, audio                      |
| TikTok      | ✅         | Public videos                                 |
| Instagram   | ✅         | Reels, posts, stories (public)                |
| Twitter/X   | ✅         | Public videos                                 |
| Facebook    | ✅         | Public videos                                 |

> For more, see the [yt-dlp supported sites list](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

---

## ⚠️ Troubleshooting

- **Errors:**  
- Make sure you are using the latest yt-dlp (`pip install -U yt-dlp`)
- Some sites may block downloads, require login, or change their backend frequently.

---

## 🛠️ Dependencies

- Python 3
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- ffmpeg
- colorama
- tqdm
- mutagen
- pydub
- termux-api (for audio playback in Termux)

The script will install these automatically, but you can also install them manually.

---

## 💡 Tips

- For **private or age-restricted content**, yt-dlp may require cookies or login.
- Always keep yt-dlp up to date for best compatibility.
- For best results on Android, use **Termux** and grant storage permissions.

---

## 🤝 Contributing

Pull requests and suggestions are welcome!  
Please open an issue for bugs or feature requests.

---

## 📜 License

MIT License

---

## 👤 Author

- Telegram: [@tron_iptv](https://t.me/tron_iptv)
- GitHub: [Matri199](https://github.com/Matri199)

---

**Enjoy downloading with MATRIX-YTD!**
