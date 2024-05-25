import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.signal import savgol_filter

df = pd.read_csv("ex10_1.tab", sep="\s+")
resol = 2033
Tmin = 698
Tmax = 973
Pmin = 1000
Pmax = 10000
levels = 15
dense = 20

T = np.linspace(Tmin, Tmax, resol)
P = np.linspace(Pmin, Pmax, resol)
Pyr = np.array(df["C[Gt(W)1]"]).reshape((resol, resol))
Pyr_sm = savgol_filter(Pyr, window_length=43, polyorder=3, axis=0)
Pyr_sm = savgol_filter(Pyr_sm, window_length=69, polyorder=2, axis=1)

fig = plt.figure(figsize=(8.4, 7))
ax = plt.subplot(box_aspect=1)
Pyr_ctf = plt.contourf(T, P, Pyr, cmap=cm.rainbow, levels=dense*levels)
plt.colorbar(Pyr_ctf)
Pyr_bound = plt.contour(T, P, Pyr, cmap=cm.rainbow, levels=dense*levels)
Pyr_cs = plt.contour(T, P, Pyr_sm, levels=levels, colors="black")
plt.clabel(Pyr_cs, fontsize=8)
plt.xlabel(r"T (K)")
plt.ylabel(r"P (bar)")
#plt.show()
plt.savefig("Pyr_isopleth.pdf", bbox_inches="tight")