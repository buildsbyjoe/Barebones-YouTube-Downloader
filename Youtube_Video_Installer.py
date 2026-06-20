# Simple Youtube video Downloader

import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk

import pathlib
from pathlib import Path

import yt_dlp

# Class

class YouTubeDownloader:

    # Initialize

    def __init__(self, root):

        self.root = root
        self.root.title("Youtube Video Downloader")
        self.root.geometry("700x350")
        self.root.resizable(False, False)

        self.download_folder = Path(__file__).parent

        self.build_ui()

    # Building UI

    def build_ui(self):

        title = tk.Label(
            self.root,
            text="Download a YouTube video or playlist",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=20)

        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="Best")

        self.url_entry = tk.Entry(
            self.root,
            textvariable=self.url_var,
            width=80
        )
        self.url_entry.pack(pady=10)

        quality_frame = tk.Frame(self.root)
        quality_frame.pack(pady=10)

        tk.Label(
            quality_frame,
            text="Quality:"
        ).pack(side=tk.LEFT, padx=5)

        self.quality_box = ttk.Combobox(
            quality_frame,
            textvariable=self.quality_var,
            values=["Best", "1080p", "720p", "480p"],
            state="readonly",
            width=10
        )
        self.quality_box.pack(side=tk.LEFT)

        folder_frame = tk.Frame(self.root)
        folder_frame.pack(pady=10)

        self.folder_label = tk.Label(
            folder_frame,
            text=f"Save to: {self.download_folder}",
            width=60,
            anchor="w"
        )
        self.folder_label.pack(side=tk.LEFT, padx=10)

        self.browse_bttn = tk.Button(
            folder_frame,
            text="Download Path",
            command=self.select_folder
        )
        self.browse_bttn.pack(side=tk.LEFT)

        self.download_bttn = tk.Button(
            self.root,
            text="Download",
            font=("Arial", 12, "bold"),
            command=self.start_download
        )
        self.download_bttn.pack(pady=10)

        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=500,
            mode="determinate"
        )
        self.progress.pack(pady=10)

        self.status_var = tk.StringVar(value="Ready")

        status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 10)
        )
        status_label.pack()

    # Selecting Download Folder

    def select_folder(self):
        folder = filedialog.askdirectory()

        if folder:
            self.download_folder = folder
            self.folder_label.config(text=f"Save to: {folder}")

    # Getting Download Format

    def get_format(self):
        formats = {
            "Best": "bv*+ba/b",
            "1080p": "bestvideo[height<=1080]+bestaudio/best",
            "720p": "bestvideo[height<=720]+bestaudio/best",
            "480p": "bestvideo[height<=480]+bestaudio/best"
        }

        return formats[self.quality_var.get()]

    # Start Downloading

    def start_download(self):
        url = self.url_var.get().strip()

        if not url:
            self.status_var.set("Please enter a valid url.")
            return

        self.download_bttn.config(state="disabled")
        self.progress["value"] = 0

        thread = threading.Thread(
            target=self.download_video,
            args=(url,),
            daemon=True
        )
        thread.start()

    # Progress Hooking

    def progress_hook(self, data):
        if data["status"] == "downloading":
            total = data.get("total_bytes") or data.get("total_bytes_estimate")

            if total:
                downloaded = data.get("downloaded_bytes", 0)
                percent = downloaded / total * 100

                self.root.after(
                    0,
                    lambda: self.progress.configure(value=percent)
                )

                speed = data.get("speed")
                eta = data.get("eta")

                status = f"Downloading... {percent:.1f}%"

                if speed:
                    status += f" | {speed / 1024 / 1024:.2f} MB/s"

                if eta:
                    status += f" | ETA: {eta}s"

                self.root.after(
                    0,
                    lambda: self.status_var.set(status)
                )

        elif data["status"] == "finished":
            self.root.after(
                0,
                lambda: self.status_var.set("Merging audio and video...")
            )

    # Download Video

    def download_video(self, url):
        options = {
            "format": self.get_format(),
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(
                self.download_folder,
                "%(title)s.%(ext)s"
            ),
            "progress_hooks": [self.progress_hook],
            "noplaylist": False,
            "quiet": True
        }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])

            self.root.after(
                0,
                lambda: self.status_var.set("Download complete.")
            )

            self.root.after(
                0,
                lambda: self.progress.configure(value=100)
            )

        except Exception as error:
            self.root.after(
                0,
                lambda: self.status_var.set(f"Error: {error}")
            )

        finally:
            self.root.after(
                0,
                lambda: self.download_bttn.config(state="normal")
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()