"""Modules to calculate the duration of the last subtitle"""
from datetime import datetime, timedelta
from itertools import islice
from pathlib import Path
from typing import Iterable, Optional


def srt_from_raw_youtube(input_text: str, seg: float = 3) -> str:
    """
    Generate an `.srt` file from a raw YouTube transcript.

    Args:
        input_text (str): The raw YouTube transcript.
        seg (float, optional): The time of the last subtitle. Defaults to 3.

    Returns:
        str: The `.srt` file.
    """
    youtube_text = input_text.splitlines()

    # Odd lines
    begin_time_stamps = youtube_text[::2]

    # Even lines
    phrases = (phrase.capitalize() for phrase in islice(youtube_text, 1, None, 2))

    end_time_stamps = _get_end_time_stamps(begin_time_stamps, seg)

    return "".join(_construct_captions(begin_time_stamps, end_time_stamps, phrases))


def _construct_captions(
    begin_time_stamps: Iterable[str],
    end_time_stamps: Iterable[str],
    phrases: Iterable[str],
) -> Iterable[str]:
    """
    Construct the captions from the begin time stamps, phrases, and end time stamps.

    Args:
        begin_time_stamps (Iterable[str]): The begin time stamps.
        end_time_stamps (Iterable[str]): The end time stamps.
        phrases (Iterable[str]): The phrases.

    Returns:
        Iterable[str]: The captions.
    """
    return (
        f"""\
{i}
00:{begin_time_stamp},00 --> 00:{end_time_stamp},00
{phrase}

"""
        for i, (begin_time_stamp, end_time_stamp, phrase) in enumerate(
            zip(begin_time_stamps, end_time_stamps, phrases), start=1
        )
    )


def get_output_file(
    input_file: Path, extension: str = "", output_file_name: Optional[str] = None
) -> Path:
    """
    Find the output file name to create a file with the same name
    but with the .srt extension and in the same directory as
    the original file.

    Parameters:
        input_file (Path): The input file path.
        extension (str, optional): The extension of the output file, by default "".
        output_file_name (str, optional): The output file name, by default None.

    Returns:
        Path: The output file path.
    """
    output_file = input_file.with_suffix(extension)
    output_file = (
        output_file.with_stem(output_file_name) if output_file_name else output_file
    )

    return output_file


def _get_end_time_stamps(begin_time_stamps: list[str], seg: float = 3) -> list[str]:
    """
    Generate the list of end time stamps for the subtitles.

    Args:
        begin_time_stamps (list[str]): The list of begin time stamps for the subtitles.
        seg (float, optional): The time of the last subtitle, by default 3.

    Returns:
        list[str]: The list of end time stamps for the subtitles.
    """
    end_time_stamps = begin_time_stamps.copy()
    end_time_stamps.pop(0)
    last_time = datetime.strptime(begin_time_stamps[-1], "%M:%S") + timedelta(
        seconds=seg
    )
    end_time_stamps.append(f"{last_time:%M:%S}")
    return end_time_stamps


def main() -> None:
    """Main program"""
    input_file = Path("src/subtitles/yt_sub.txt")
    input_text: str = input_file.read_text(encoding="utf-8")
    output_text: str = srt_from_raw_youtube(input_text=input_text)
    output_file: Path = get_output_file(input_file, extension=".srt")
    output_file.write_text(output_text, encoding="utf-8")


if __name__ == "__main__":
    main()
