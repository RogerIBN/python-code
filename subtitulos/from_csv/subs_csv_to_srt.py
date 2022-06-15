from datetime import datetime, timedelta
import pandas as pd

data = pd.read_csv("subtitulos/from_csv/tiempo_frase.txt", encoding="utf-8")

tiempo = data["tiempo"].values
frase = data["frase"].values

for i in range(len(tiempo)):
    print(i + 1)
    try:
        primer_t = f"00:{tiempo[i]},00"
        segundo_t = f"00:{tiempo[i + 1]},00"
        print(primer_t + " --> " + segundo_t)
        print(frase[i].capitalize() + "\n")
    except:
        ultimo_t = datetime.strptime(tiempo[i], "%M:%S")
        ultimo_t += timedelta(seconds=3)
        print(f"00:{tiempo[i]},00 --> {ultimo_t.strftime('%H:%M:%S')},00")
        print(frase[i].capitalize())
