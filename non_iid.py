#!/bin/python3

from subprocess import Popen, PIPE
import json

PROJECT_DIR = "/home/james/Desktop/Project"


def gen_filename(intensity, temp=None):
    if not temp:
        return f"{PROJECT_DIR}/Reshaped/AmbientT_dc{intensity}raw.bin"
    return f"{PROJECT_DIR}/Reshaped/75degT_dc{intensity}raw.bin"


def run(ambient):
    results = []
    for dc in range(48, 69):
        filename = gen_filename(dc, sample_size, ambient)
        print(f"Running test ea_non_iid on {filename}")
        with Popen(["ea_non_iid", filename], stdout=PIPE, stdin=PIPE) as process:
            stdout, _stderr = process.communicate()
            lines = stdout.decode("utf-8").split("\n")
            lines = lines[-4:-1]
            vals = [float(line.split(" ")[-1]) for line in lines if len(line) > 2]
            result = {"original": vals[0], "bitstring": vals[1]}
            results.append(result)
    return results


with open("Ambient.json", "w") as file:
    json.dump(run(True), file)
with open("75deg.json", "w") as file:
    json.dump(run(False), file)
