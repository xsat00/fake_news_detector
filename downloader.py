import yt_dlp
import os

def downloads(url, save_path=r"C:\Users\Sathwik\myprojects\Vid"):
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'format': 'best',
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', 'Unknown Title')
            filename = ydl.prepare_filename(info_dict)
            print(f"Downloaded to: {filename}")
            return filename, title

    except Exception as e:
        print("Download Failed:", e)
        return None, None
