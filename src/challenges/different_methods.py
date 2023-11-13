"""
This solves the challenge in 3 different ways.
"""
from statistics import mean

import numpy as np
import pandas as pd

heights_inches = [71, 75, 68, 72, 73]
weight_pounds = [165, 190, 140, 175, 185]

# Using Pandas
df = pd.DataFrame({"heights_inches": heights_inches, "weight_pounds": weight_pounds})
pandas_ans = df.loc[lambda df_: df_["heights_inches"] > 71, "weight_pounds"].mean()

# Using Numpy
metrics = np.array(
    list(zip(heights_inches, weight_pounds)),
    dtype=[("heights_inches", int), ("weight_pounds", int)],
)
numpy_ans = metrics["weight_pounds"].mean(where=metrics["heights_inches"] > 71)

# Using Python
python_ans = mean(
    weight for height, weight in zip(heights_inches, weight_pounds) if height > 71
)
print(f"{pandas_ans=}, {numpy_ans=}, {python_ans=}")
