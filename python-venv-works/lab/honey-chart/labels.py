# Labels for this year's honey jars (new code: numpy 2's string functions).
import numpy as np

jars = np.array(["clover", "heather", "lime"])
print("Jar labels:", ", ".join(np.strings.upper(jars)))
