"""Módulos para calcular el la duración del último subtítulo"""
from datetime import datetime, timedelta
from pathlib import Path


def subconv(archivo: str, nombre: str = None, seg: int = 3):
    """
    Crea un archivo de extensión srt tomando un archivo de script de
    youtube.
    Args:
        archivo (str): Dirección del archivo.
        seg (int, opcional): Duración del último subtítulo.
        Defaults to 3.
        nombre (str, opcional): Nombre del archivo.
        Defaults to original name.
    """
    # Busca el nombre del archivo para crear uno que se llame igual
    # pero con extensión .srt y en la misma dirección del
    # archivo original

    resultado = Path(archivo).with_suffix(".srt")

    if nombre:  # Si le metiste un nombre al archivo de salida
        resultado = resultado.with_stem(nombre)

    # Lee los subtitulos y crea el nuevo archivo
    with (
        open(archivo, "r", encoding="utf-8") as txt,
        open(resultado, "w", encoding="utf-8") as srt,
    ):
        # Separa los tiempos de las frases en una tupla para tiempos
        # y en un generador para las frases
        txt = tuple(txt)
        # Impares
        tiempos = tuple(tiempo.rstrip() for tiempo in txt[::2])
        # Pares
        frases = (frase.rstrip().capitalize() for frase in txt[1::2])

        for i, frase in enumerate(frases):
            # Escribe el número de subtítulo
            srt.write(str(i + 1))
            try:
                # Da formato a los tiempos
                primer_t = f"00:{tiempos[i]},00"
                segundo_t = f"00:{tiempos[i + 1]},00"

                # Escribe el la duración del sub y la frase
                srt.write(f"\n{primer_t} --> {segundo_t}\n")
                srt.write(frase + "\n" * 2)

            except IndexError:  # Justo cuando falte el último tiempo
                # Tomando el último tiempo del archivo se le da formato
                # y suma 'seg' segundos para obtener el momento cuando
                # desaparece el último subtítulo
                penúltimo_t = f"00:{tiempos[i]},00"
                ultimo_t = datetime.strptime(tiempos[i], "%M:%S")
                ultimo_t += timedelta(seconds=seg)
                ultimo_t = f"{ultimo_t.strftime('%H:%M:%S')},00"

                # Se escribe el intervalo con su frase
                srt.write(f"\n{penúltimo_t} --> {ultimo_t}\n")
                srt.write(frase)


def main():
    """Programa principal"""
    subconv("subtitulos/from_txt/yt_sub.txt")


if __name__ == "__main__":
    main()
