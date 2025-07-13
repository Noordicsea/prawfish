import yt_dlp

def download_media_from_link(link, output_path="downloads/%(title)s.%(ext)s"):
    """
    Downloads media from a given link using yt_dlp at the highest quality.
    Handles non-YouTube links and avoids fragment failure.

    Args:
        link (str): The URL to download media from.
        output_path (str): The output template for the downloaded file.

    Returns:
        str: The path to the downloaded file, or None if failed.
    """
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'ignoreerrors': True,
        'retries': 10,
        'fragment_retries': 20,
        'continuedl': True,
        'quiet': True,
        'nooverwrites': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.download([link])
            return output_path if result == 0 else None
        except Exception:
            return None
