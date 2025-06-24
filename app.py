import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from yt_dlp import YoutubeDL

app = Flask(__name__)
CORS(app)

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    platform = data.get("platform")

    if not url or platform not in ["youtube", "instagram"]:
        return jsonify({"error": "Invalid platform or URL"}), 400

    ydl_opts = {
        "format": "best",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "outtmpl": "%(id)s.%(ext)s"
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            download_url = info.get("url")

            return jsonify({
                "success": True,
                "platform": platform,
                "title": info.get("title", "Video"),
                "download_link": download_url
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
