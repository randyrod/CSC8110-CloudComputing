import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time

timeStampFormat = "%Y-%m-%dT%H:%M:%S.%f"


def convert_to_epoch(convert_date):
    return (convert_date - datetime(1970, 1, 1)).total_seconds()


dt = datetime.now()

print datetime(1970, 1, 1)
print datetime.min

print dt.total_seconds()

print convert_to_epoch(dt)
'''
x = np.linspace(0, 2)
plt.plot(x, x, label="linear")
plt.plot(x, x**2, label="quadratic")

plt.xlabel("x label")
plt.ylabel("y label")

plt.title("Something")

plt.legend()

plt.show()
'''
