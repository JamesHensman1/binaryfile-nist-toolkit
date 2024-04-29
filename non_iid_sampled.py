#!/bin/python3

from subprocess import Popen, PIPE
import json
import numpy as np

def ah(i: int):
    if i < 1e3:
        return str(i)
    elif i < 1e6:
        return str(i//1e3) + 'K'
    elif i < 1e9:
        return str(i//1e6) + 'M'
    else:
        return str(i)

PROJECT_DIR = "/home/james/Desktop/Project"
SAMPLE_SIZES = np.array([1024, 5120, 2e4, 1e5, 3e5, 6e5, 1e6], dtype=np.dtype('uint32'))//2


def gen_filename(intensity, sample_size, ambient):
    if ambient:
        return f'{PROJECT_DIR}/Reshaped/Samples/Ambient/{sample_size}/AmbientT_dc{intensity}_{sample_size}.bin'
    return f'{PROJECT_DIR}/Reshaped/Samples/75deg/{sample_size}/75degT_dc{intensity}_{sample_size}.bin'

def run(ambient):
    samples = {}
    for size in SAMPLE_SIZES:
        sample_size = ah(2*size)
        sample = []
        for dc in range(48,69):
            filename = gen_filename(dc, sample_size, ambient)
            print(f"Running test ea_non_iid on {filename}")
            with Popen(
            [
                'ea_non_iid',
                filename
            ],
            stdout=PIPE,
            stdin=PIPE) as process:
                stdout, _stderr = process.communicate()
                lines = stdout.decode("utf-8").split("\n")
                lines = lines[-4:-1]
                vals = [float(line.split(" ")[-1]) for line in lines if len(line) > 2]
                result = {'original': vals[0], 'bitstring': vals[1]}
                sample.append(result)
        samples[sample_size] = sample
    return samples

with open('75degSamples.json','w') as file:
    json.dump(run(False), file)
with open('AmbientSamples.json','w') as file:
    json.dump(run(True), file)