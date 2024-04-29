import numpy as np

mbit = 5
PROJECT_DIR = "/home/james/Desktop/Project"

for dc in range(48, 69):
    data = np.fromfile(
        f"{PROJECT_DIR}/Data/STM32F756_AmbientT_dc{dc}.bin",
        dtype=np.dtype("uint8"),
    )
    data = data[::2]
    data = np.unpackbits(data)
    data = data.reshape(len(data) // 8, 8)[:, 3:]
    data = data.reshape(int(len(data) / (8 / 5)), 8)
    data = np.packbits(data)

    with open(
        f"{PROJECT_DIR}/Reshaped/AmbientT_dc{dc}_raw.bin",
        "w",
    ) as file:
        data.tofile(file)

# Ambient
for dc in range(48, 69):
    data = np.fromfile(
        f"{PROJECT_DIR}/Data/STM32F756_75degT_dc{dc}.bin",
        dtype=np.dtype("uint8"),
    )
    data = data[::2]
    data = np.unpackbits(data)
    data = data.reshape(len(data) // 8, 8)[:, 3:]
    data = data.reshape(int(len(data) / (8 / 5)), 8)
    data = np.packbits(data)

    with open(
        f"{PROJECT_DIR}/Reshaped/75degT_dc{dc}_raw.bin",
        "w",
    ) as file:
        data.tofile(file)
