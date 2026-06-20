# YouTube Video Downloader 🎥⬇️

## Overview
This project is a simple desktop application built using Python and Tkinter that allows users to download YouTube videos or playlists in different quality options. It uses `yt-dlp` as the core download engine and provides a lightweight GUI for ease of use.

---

## Tools used
- Python
- Tkinter (GUI)
- yt-dlp
- threading module
- os module
- pathlib module

---

## Features
- Download YouTube videos or playlists via URL
- Select video quality:
  - Best available
  - 1080p
  - 720p
  - 480p
- Choose custom download directory
- Real-time progress bar with:
  - Download percentage
  - Speed indicator
  - ETA
- Background threading (prevents GUI freezing)
- Automatic merging of audio + video (MP4 output)
- Displays download status updates in real time

---

## Output
- Downloads are saved to the selected folder
- Default save location is the script directory
- Files are named using the video title
- Final output format: `.mp4`

---

## How to run
1) Install Python (3.8+ recommended)

2) Install dependencies:
```bash
pip install yt-dlp

## Legal Notice

This project is intended strictly for educational and personal use only.

I, Joe Clakre, does not endorse, encourage, or support piracy
Users are responsible for ensuring they comply with YouTube’s Terms of Service and local copyright laws
This tool should not be used to download copyrighted content without permission
I, Joe Clarke, assumes no liability for misuse of this software

By using this software, you agree that you are solely responsible for how it is used.
