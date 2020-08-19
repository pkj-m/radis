import os
import numpy as np

np_dir = "./npy-sub/"
fnames = sorted([f for f in os.listdir(np_dir) if f[-3:] == "npy"])[::-1]

size = 0
max_size = 123768884

names = ["v0", "da", "S0", "El", "Eu", "log_2gs", "na", "log_2vMm"]

data = np.zeros((8, max_size), dtype=np.float32)

for fname in fnames[::-1]:
    temp = np.load(np_dir + fname)

    data[:, size : size + len(temp[0])] = temp
    size += len(temp[0])
    print(fname, size, size * 32)

for i in range(len(names)):
    np.save(names[i] + ".npy", data[i])
    print(names[i])

# Per line, the following data is needed:
# v0
# da
# S0
# El
# Eu
# log_2gs
# na
# log_2vMm

# There are 8 x 4 = 32 Byte per line for equilibrium spectra

# There is 8192 MB (8,589,934,592 bytes) available on the RTX-2070mq
# We therefore limit the spectral range between 2400..1750cm-1,
# resulting in 251,245,187 lines, needing 8,039,845,984 bytes.
# This leaves plenty of space for the DLM and lineshape prototypes.
# Distributed over the 2304 CUDA cores, this amounts to 109,048 lines
# per core.
