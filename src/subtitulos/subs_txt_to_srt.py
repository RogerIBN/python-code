# %%
"""Módulos para calcular el la duración del último subtítulo"""
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Sequence

# %%


def srt_from_raw_youtube(
    archivo_entrada: str, nombre: Optional[str] = None, seg: float = 3
) -> None:
    """
    Crea un archivo de extensión srt tomando un archivo de script de
    youtube.
    Args:
        archivo_entrada (str): Dirección del archivo.
        nombre (str, opcional): Nombre del archivo.
        Defaults to original name.
        seg (float): Duración del último subtítulo.
        Default de 3.
    """
    # Busca el nombre del archivo para crear uno que se llame igual
    # pero con extensión .srt y en la misma dirección del
    # archivo original

    archivo_salida = Path(archivo_entrada).with_suffix(".srt")
    archivo_salida = archivo_salida.with_stem(nombre) if nombre else archivo_salida

    # Lee los subtítulos y crea el nuevo archivo
    with (
        open(archivo_entrada, "r", encoding="utf-8") as txt,
        open(archivo_salida, "w", encoding="utf-8") as srt,
    ):
        # Separa los tiempos de las frases en una tupla para tiempos
        # y en un generador para las frases
        txt = tuple(line.rstrip() for line in txt.readlines())
        # Impares
        tiempos = txt[::2]
        # Pares
        frases = (frase.capitalize() for frase in txt[1::2])

        for i, frase in enumerate(frases):
            # Escribe el número de subtítulo
            srt.write(str(i + 1))
            primer_t = f"00:{tiempos[i]},00"
            segundo_t = get_second_time(tiempos, i, seg)
            # Escribe el la duración del sub y la frase
            srt.write(f"\n{primer_t} --> {segundo_t}\n")
            srt.write(frase + "\n" * 2)


def get_second_time(tiempos: Sequence[str], i: int, last_seg: float) -> str:
    """Obtiene el segundo tiempo de la lista de tiempos para el subtítulo actual

    Args:
        tiempos (Sequence[str]): Los tiempos de los subtítulos
        i (int): Contador del subtítulo actual
        last_seg (float): Duración del último subtítulo

    Returns:
        srt: Segundo tiempo
    """
    try:
        # Da formato a los tiempos
        return f"00:{tiempos[i + 1]},00"

    except IndexError:  # Justo cuando falte el último tiempo
        # Tomando el último tiempo del archivo se le da formato
        # y suma 'last_seg' segundos para obtener el momento cuando
        # desaparece el último subtítulo
        segundo_t = datetime.strptime(tiempos[i], "%M:%S") + timedelta(seconds=last_seg)
        return f"{segundo_t.strftime('%H:%M:%S')},00"

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
