import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.spatial import distance

df = pd.read_csv("ex10_1.tab", sep="\s+")
resol = 2033
Tmin = 698
Tmax = 973
Pmin = 1000
Pmax = 10000

T = np.linspace(Tmin, Tmax, resol)
P = np.linspace(Pmin, Pmax, resol)
Pyr = np.array(df["C[Gt(W)1]"]).reshape((resol, resol))
Pyr_sm = savgol_filter(Pyr, window_length=19, polyorder=1, axis=0)
Pyr_sm = savgol_filter(Pyr_sm, window_length=28, polyorder=1, axis=1)
Grs = np.array(df["C[Gt(W)2]"]).reshape((resol, resol))
Grs_sm = savgol_filter(Grs, window_length=30, polyorder=1, axis=0)
Grs_sm = savgol_filter(Grs_sm, window_length=31, polyorder=1, axis=1)

fig = plt.figure(figsize=(7, 7))
ax = plt.subplot(box_aspect=1)
Pyr_cs = plt.contour(T, P, Pyr_sm, levels=[0.02, 0.08, 0.18], alpha=0)
Grs_cs = plt.contour(T, P, Grs_sm, levels=[0.06, 0.16, 0.38], alpha=0)

Pyr_segs = Pyr_cs.allsegs
Grs_segs = Grs_cs.allsegs
Ts = np.zeros(3)
Ps = np.zeros(3)
for i in range(3):
    Pyrline = np.concatenate(Pyr_segs[i])
    Grsline = np.concatenate(Grs_segs[2 - i])
    dist_matrix = distance.cdist(Pyrline, Grsline, "euclidean")
    min_index = np.unravel_index(np.argmin(dist_matrix), dist_matrix.shape)
    closest_Pyr = Pyrline[min_index[0]]
    closest_Grs = Grsline[min_index[1]]
    Ts[i], Ps[i] = (closest_Pyr + closest_Grs) / 2

part = ["core", "mantle", "rim"]
with open("PT_path.txt", "w") as file:
    for i in range(3):
        file.write("P-T condition of {}:\n".format(part[i]))
        file.write("\tTemperature = {} K\n".format(Ts[i]))
        file.write("\tPressure = {} bar\n".format(Ps[i]))
        
plt.quiver(Ts[:-1], Ps[:-1], Ts[1:]-Ts[:-1], Ps[1:]-Ps[:-1], scale_units="xy", angles="xy", scale=1)
plt.scatter(Ts, Ps, color="red", zorder=4)
plt.annotate(part[0], (Ts[0] - 18, Ps[0] + 50))
plt.annotate(part[1], (Ts[1] - 26, Ps[1] + 100))
plt.annotate(part[2], (Ts[2] + 4, Ps[2] - 10))
plt.clabel(Pyr_cs, fontsize=8)
plt.clabel(Grs_cs, fontsize=8)
plt.xticks([])
plt.yticks([])
#plt.show()
plt.savefig("PT_path_transparent.png", dpi=1200, bbox_inches="tight", transparent=True)