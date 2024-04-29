import numpy as np
import os

PROJECT_DIR = "/home/james/Desktop/Project"  # Change me
SAMPLE_DIR = f"{PROJECT_DIR}/Samples"
SAMPLE_DIR_RAW = f"{PROJECT_DIR}/Reshaped/Samples"

SAMPLE_SIZES = (
    np.array([1024, 5120, 2e4, 1e5, 3e5, 6e5, 1e6], dtype=np.dtype("uint32")) // 2
)


def ah(i: int):
    if i < 1e3:
        return str(i)
    elif i < 1e6:
        return str(i // 1e3) + "K"
    elif i < 1e9:
        return str(i // 1e6) + "M"
    else:
        return str(i)


for dc in range(48, 69):
    data1 = np.fromfile(
        f"{PROJECT_DIR}/Data/STM32F756_AmbientT_dc{dc}.bin",
        dtype=np.dtype("uint16"),
    )
    data2 = np.fromfile(
        f"{PROJECT_DIR}/Data/STM32F756_75degT_dc{dc}.bin",
        dtype=np.dtype("uint16"),
    )
    for size in SAMPLE_SIZES:
        sample_size = ah(2 * size)
        print(f"Sample Size {sample_size}")

        if not os.path.exists(f"{SAMPLE_DIR}/Ambient/{sample_size}"):
            os.mkdir(f"{SAMPLE_DIR}/Ambient/{sample_size}")
        if not os.path.exists(f"{SAMPLE_DIR}/75deg/{sample_size}"):
            os.mkdir(f"{SAMPLE_DIR}/75deg/{sample_size}")
        if not os.path.exists(f"{SAMPLE_DIR_RAW}/Ambient/{sample_size}"):
            os.mkdir(f"{SAMPLE_DIR_RAW}/Ambient/{sample_size}")
        if not os.path.exists(f"{SAMPLE_DIR_RAW}/75deg/{sample_size}"):
            os.mkdir(f"{SAMPLE_DIR_RAW}/75deg/{sample_size}")

        with open(
            f"{SAMPLE_DIR}/Ambient/{sample_size}/AmbientT_dc{dc}_{sample_size}.bin", "w"
        ) as file:
            np.random.choice(data1, size, replace=False).tofile(file)
        with open(
            f"{SAMPLE_DIR}/75deg/{sample_size}/75degT_dc{dc}_{sample_size}.bin", "w"
        ) as file:
            np.random.choice(data2, size, replace=False).tofile(file)

        data1raw = np.unpackbits(data1.astype(np.uint8))
        data1raw = data1raw.reshape(len(data1raw) // 8, 8)[:, 3:].flatten()
        while len(data1raw) % 8 != 0:
            data1raw = data1raw[:-1]
        data1raw = data1raw.reshape(len(data1raw) // 8, 8)
        data1raw = np.packbits(data1raw)

        data2raw = np.unpackbits(data2.astype(np.uint8))
        data2raw = data2raw.reshape(len(data2raw) // 8, 8)[:, 3:].flatten()
        while len(data2raw) % 8 != 0:
            data2raw = data2raw[:-1]
        data2raw = data2raw.reshape(len(data2raw) // 8, 8)
        data2raw = np.packbits(data2raw)

        with open(
            f"{SAMPLE_DIR_RAW}/Ambient/{sample_size}/AmbientT_dc{dc}_{sample_size}.bin",
            "w",
        ) as file:
            np.random.choice(data1raw, size * 2, replace=False).tofile(file)
        with open(
            f"{SAMPLE_DIR_RAW}/75deg/{sample_size}/75degT_dc{dc}_{sample_size}.bin", "w"
        ) as file:
            np.random.choice(data2raw, size * 2, replace=False).tofile(file)
