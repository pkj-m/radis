import numpy as np
import os
from scipy.constants import c, k, N_A, pi

c_cm = c * 100


def import_HITRAN(fnames):
    iso, v0, A21, gs, El, na, da, gu = [], [], [], [], [], [], [], []

    fnames = [fnames] if type(fnames) == str else sorted(fnames)

    for fname in fnames:
        # print("Loading " + fname + "...")
        with open(fname, "r") as f:
            for line in f:
                if len(line) > 10:
                    iso.append(int(line[2:3]))  # iso
                    v0.append(float(line[3:15]))  # v0
                    A21.append(float(line[25:35]))  # A21
                    gs.append(float(line[40:45]))  # gamma_self
                    El.append(float(line[45:55]))  # Elow
                    na.append(float(line[55:59]))  # n_air
                    da.append(float(line[59:67]))  # d_air

                    DJ = ord(line[117:118]) - ord("Q")
                    Jl = int(line[118:121])  # d_air
                    Ju = Jl + DJ

                    gu.append(2 * Ju + 1)  # g_up

    return np.array([iso, v0, A21, gs, El, na, da, gu])


def load_HITRAN(fname):
    data = import_HITRAN(fname)
    data = data[:, data[0] <= 3]  # select only first three isotopes
    iso, v0, A21, gs, El, na, da, gu = data

    Mm = (np.array([44, 45, 46]) * 1e-3 / N_A)[iso.astype(int) - 1]
    f_ab = np.array([0.98420, 0.01106, 0.0039471])[iso.astype(int) - 1]
    Eu = El + v0
    S0 = f_ab * gu * A21 / (8 * pi * c_cm * v0 ** 2)

    log_2gs = np.log(2 * gs)  # vector
    log_2vMm = np.log(2 * v0) + 0.5 * np.log(
        2 * k * np.log(2) / (c ** 2 * Mm)
    )  # vector

    return np.array([v0, da, S0, El, Eu, log_2gs, na, log_2vMm], dtype=np.float32)


par_folder = "./par/"
npy_folder = "./npy/"

if not os.path.exists(npy_folder):
    os.mkdir(npy_folder)

read_list = sorted(os.listdir(par_folder))[::-1]
write_list = os.listdir(npy_folder)

for fname in read_list:
    print(fname, end=" ")
    if fname + ".npy" not in write_list:
        data = load_HITRAN(par_folder + fname)
        np.save(npy_folder + fname + ".npy", data)
        print(len(data[0]))
    else:
        print("...Skipping!")
