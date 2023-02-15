# %%
"""Módulos para calcular el la duración del último subtítulo"""
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Sequence

# %%


def srt_from_raw_youtube(
    input_file: str, name: Optional[str] = None, seg: float = 3
) -> None:
    """
    Crea un archivo de extensión srt tomando un archivo de script de youtube.

    Parameters
    ----------
    input_file : str
        Dirección del archivo.
    name : Optional[str], optional
        Nombre del archivo, by default None
    seg : float, optional
        Duración del último subtítulo, by default 3
    """
    # Busca el nombre del archivo para crear uno que se llame igual
    # pero con extensión .srt y en la misma dirección del
    # archivo original

    output_file = Path(input_file).with_suffix(".srt")
    output_file = output_file.with_stem(name) if name else output_file

    # Lee los subtítulos y crea el nuevo archivo
    with (
        open(input_file, "r", encoding="utf-8") as txt,
        open(output_file, "w", encoding="utf-8") as srt,
    ):
        # Separa los tiempos de las frases en una tupla para tiempos
        # y en un generador para las frases
        txt = tuple(line.rstrip() for line in txt.readlines())
        # Impares
        time_stamps = txt[::2]
        # Pares
        phrases = (phrase.capitalize() for phrase in txt[1::2])

        for i, phrase in enumerate(phrases):
            # Escribe el número de subtítulo
            srt.write(str(i + 1))
            first_time = f"00:{time_stamps[i]},00"
            second_time = get_second_time(time_stamps, i, seg)
            # Escribe el la duración del sub y la frase
            srt.write(f"\n{first_time} --> {second_time}\n")
            srt.write(phrase + "\n" * 2)


def get_second_time(time_stamps: Sequence[str], i: int, last_second: float) -> str:
    """
    Obtiene el segundo tiempo de la lista de tiempos para el subtítulo actual.

    Parameters
    ----------
    time_stamps : Sequence[str]
        Los tiempos de los subtítulos
    i : int
        Contador del subtítulo actual
    last_second : float
        Duración del último subtítulo

    Returns
    -------
    str
        Segundo tiempo
    """
    try:
        # Da formato a los tiempos
        return f"00:{time_stamps[i + 1]},00"

    except IndexError:  # Justo cuando falte el último tiempo
        # Tomando el último tiempo del archivo se le da formato
        # y suma 'last_seg' segundos para obtener el momento cuando
        # desaparece el último subtítulo
        second_time = datetime.strptime(time_stamps[i], "%M:%S") + timedelta(
            seconds=last_second
        )
        return f"{second_time:%H:%M:%S},00"

    except ValueError:
        # Si no se puede dar formato a los tiempos
        print("Error: Tiempos inválidos")
        sys.exit()


def main() -> None:
    """Programa principal"""
    srt_from_raw_youtube("src/subtitulos/yt_sub.txt")


# %%

if __name__ == "__main__":
    main()

# %%
