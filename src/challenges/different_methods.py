"""
Python Question
What method would you pick to solve this problem?
First, pick the method, then provide solution.🤔🤔

>>> heights_inches = [ 71,  75,  68,  72,  73]
>>> weight_pounds  = [165, 190, 140, 175, 185]

What is the average weight of the persons with height above 71 inches?
How are you solving this problem?
- (A) Solve the problem using pandas.
- (B) Solve the problem using NumPy.
- (c) Solve the problem using pure Python.

Now, provide the answer using the method you picked.
> Benjamin Bennett Alexander (@RealBenjizo)
> [May 19, 2023](https://twitter.com/RealBenjizo/status/1659634156949610508?ref_src=twsrc%5Etfw)
"""
from statistics import mean

import numpy as np
import pandas as pd

heights_inches = [71, 75, 68, 72, 73]
weight_pounds = [165, 190, 140, 175, 185]

# Using Pandas
df = pd.DataFrame({"heights_inches": heights_inches, "weight_pounds": weight_pounds})
serie: pd.Series = df.loc[lambda df_: df_["heights_inches"] > 71, "weight_pounds"]  # type: ignore
pandas_ans = serie.mean()

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
print(__doc__)
