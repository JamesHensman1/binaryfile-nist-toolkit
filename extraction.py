import hashlib
import numpy as np

PROJECT_DIR = '/home/james/Desktop/Project'
NIN = 42


for dc in range(48, 69):
    data = np.fromfile(
        f"{PROJECT_DIR}/Reshaped/AmbientT_dc{dc}raw.bin",
        dtype=np.dtype("uint8"),
    )
    length = len(data) // NIN
    data = data[:-(len(data)%NIN)]
    data = data.reshape(length, NIN) 
    data = np.array(
        [
            np.frombuffer(hashlib.sha256(chunk.tobytes()).digest(), dtype=np.dtype("uint8"))
            for chunk in data
        ]
    )
    data = data.flatten()
    with open(
        f"{PROJECT_DIR}/Reshaped/AmbientT_dc{dc}_extracted.bin",
        "wb",
    ) as file:
        data.tofile(file)
    data = np.fromfile(
        f"{PROJECT_DIR}/Data/STM32F756_75degT_dc{dc}.bin",
        dtype=np.dtype("uint8"),
    )
    data = data.tobytes()
    length = len(data) // NIN
    data = [data[i * NIN : (i * NIN) + NIN-1] for i in range(length)]
    data = np.array(
        [
            np.frombuffer(hashlib.sha256(b).digest(), dtype=np.dtype("uint8"))
            for b in data
        ]
    )
    data = data.flatten()
    with open(
        f"{PROJECT_DIR}/Extractions/75deg/75degT_dc{dc}_extracted.bin",
        "wb",
    ) as file:
        data.tofile(file)