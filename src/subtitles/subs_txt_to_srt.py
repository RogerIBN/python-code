"""Módulos para calcular el la duración del último subtítulo"""
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, Optional


def srt_from_raw_youtube(
    input_file: Path, output_file_name: Optional[str] = None, seg: float = 3
) -> None:
    """
    Crea un archivo de extensión srt tomando un archivo de script de youtube.

    Parameters
    ----------
    input_file : str
        Dirección del archivo.
    output_file_name : Optional[str], optional
        Nombre del archivo, by default None
    seg : float, optional
        Duración del último subtítulo, by default 3
    """
    # Busca el nombre del archivo para crear uno que se llame igual
    # pero con extensión .srt y en la misma dirección del
    # archivo original

    output_file = get_output_file(input_file, output_file_name)

    # Lee los subtítulos y crea el nuevo archivo
    with input_file.open("r", encoding="utf-8") as txt:
        txt = [line.rstrip() for line in txt.readlines()]

    # Separa los tiempos de las frases en una tupla para tiempos
    # y en un generador para las frases

    # Impares
    begin_time_stamps = txt[::2]
    # Pares
    phrases = (phrase.capitalize() for phrase in txt[1::2])

    captions = get_captions(begin_time_stamps, phrases, seg)

    with output_file.open("w", encoding="utf-8") as srt:
        srt.writelines(captions)


def get_captions(
    begin_time_stamps: list[str], phrases: Iterable[str], seg: float
) -> list[str]:
    """
    Crear las líneas del archivo srt.

    Parameters
    ----------
    begin_time_stamps : list[str]
        La lista de tiempos iniciales de los subtítulos.
    phrases : Iterable[str]
        El generador de frases.
    seg : float
        La duración del último subtítulo.

    Returns
    -------
    list[str]
        La lista de líneas del archivo srt.
    """
    end_time_stamps = get_end_time_stamps(begin_time_stamps, seg)

    captions = []
    for i, (begin_time_stamp, end_time_stamp, phrase) in enumerate(
        zip(begin_time_stamps, end_time_stamps, phrases), start=1
    ):
        caption = f"""\
{i}
00:{begin_time_stamp},00 --> 00:{end_time_stamp},00
{phrase}
"""
        captions.append(caption)
    return captions


def get_output_file(input_file: Path, output_file_name: Optional[str]) -> Path:
    """
    Genera la dirección del archivo de salida.

    Parameters
    ----------
    input_file : Path
        Dirección del archivo de entrada.
    output_file_name : str
        Nombre del archivo de salida.

    Returns
    -------
    Path
        Dirección del archivo de salida.
    """
    output_file = input_file.with_suffix(".srt")
    output_file = (
        output_file.with_stem(output_file_name) if output_file_name else output_file
    )

    return output_file


def get_end_time_stamps(begin_time_stamps: list[str], seg: float = 3) -> list[str]:
    """
    Genera la lista de tiempos finales de los subtítulos.

    Parameters
    ----------
    begin_time_stamps : list[str]
        La lista de tiempos iniciales de los subtítulos.
    seg : float, optional
        El tiempo del último subtítulo, by default 3

    Returns
    -------
    list[str]
        La lista de tiempos finales de los subtítulos.
    """
    end_time_stamps = begin_time_stamps.copy()
    end_time_stamps.pop(0)
    last_time = datetime.strptime(begin_time_stamps[-1], "%M:%S") + timedelta(
        seconds=seg
    )
    end_time_stamps.append(f"{last_time:%M:%S}")
    return end_time_stamps


def main() -> None:
    """Programa principal"""
    srt_from_raw_youtube(Path("src/subtitulos/yt_sub.txt"))


if __name__ == "__main__":
    main()