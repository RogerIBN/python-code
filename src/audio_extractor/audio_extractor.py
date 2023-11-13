"""
Extrae el audio de un video y lo guarda en un archivo mp3.
"""
from pathlib import Path

from moviepy.editor import VideoFileClip


def main():
    """
    Función principal del programa.
    """
    video_path = Path("C:/Users/rogab/Downloads/VID_20231015_170918.mp4")
    if not video_path.exists():
        print("The video file doesn't exist.")
        return
    audio_path = video_path.with_name(f"{video_path.stem}_audio").with_suffix(".mp3")

    with VideoFileClip(str(video_path)) as video:
        if audio := video.audio:
            audio.write_audiofile(str(audio_path))
        else:
            print("No audio found in the video file.")


if __name__ == "__main__":
    main()
