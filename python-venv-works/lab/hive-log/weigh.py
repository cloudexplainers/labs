# The beekeeping club's hive scale: this week's weights for hive 3, in kilograms (written in 2023, numpy 1).
import numpy as np

weights = np.array([31.2, 32.0, 33.4, 35.1], dtype=np.float_)
print(f"Hive 3 gained {weights[-1] - weights[0]:.1f} kg this week")
