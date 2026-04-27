
from flask import Flask, render_template, request, redirect, flash
import yt_dlp
import os


app = Flask(__name__)
app.secret_key = "secret"

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download/video", methods=["POST"])
def download_video():
    url = request.form.get("url")

    if not url:
        flash("Please enter a URL")
        return redirect("/")

    try:
        ydl_opts = {
            "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
            "format": "bestvideo+bestaudio/best",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        flash("Video downloaded successfully!")

    except Exception as e:
        flash(str(e))

    return redirect("/")


@app.route("/download/audio", methods=["POST"])
def download_audio():
    url = request.form.get("url")

    if not url:
        flash("Please enter a URL")
        return redirect("/")

    try:
        ydl_opts = {
            "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        flash("Audio downloaded successfully!")

    except Exception as e:
        flash(str(e))

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)