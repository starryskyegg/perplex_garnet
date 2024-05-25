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
levels = 20
dense = 20

T = np.linspace(Tmin, Tmax, resol)
P = np.linspace(Pmin, Pmax, resol)
Grs = np.array(df["C[Gt(W)2]"]).reshape((resol, resol))
Grs_sm = savgol_filter(Grs, window_length=43, polyorder=3, axis=0)
Grs_sm = savgol_filter(Grs_sm, window_length=69, polyorder=2, axis=1)

fig = plt.figure(figsize=(8.4, 7))
ax = plt.subplot(box_aspect=1)
Grs_ctf = plt.contourf(T, P, Grs, cmap=cm.rainbow, levels=dense*levels)
plt.colorbar(Grs_ctf)
Grs_bound = plt.contour(T, P, Grs, cmap=cm.rainbow, levels=dense*levels)
Grs_cs = plt.contour(T, P, Grs_sm, levels=levels, colors="black")
plt.clabel(Grs_cs, fontsize=8)
plt.xlabel(r"T (K)")
plt.ylabel(r"P (bar)")
#plt.show()
plt.savefig("Grs_isopleth.pdf", bbox_inches="tight")