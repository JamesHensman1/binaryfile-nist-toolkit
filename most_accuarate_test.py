from subprocess import Popen, PIPE
import numpy as np

PROJECT_DIR = "/home/james/Desktop/Project"
DATA_DIR = "{PROJECT_DIR}/Reshaped"
SAMPLE_DIR = "{PROJECT_DIR}/Reshaped/Samples"


def gen_files():

    files = (
        [f"{DATA_DIR}/AmbientT_dc{dc}raw.bin" for dc in range(48, 69)]
        + [f"{DATA_DIR}/75degT_dc{dc}raw.bin" for dc in range(48, 69)]
        + [
            f"{SAMPLE_DIR}/Ambient/{size}/AmbientT_dc{dc}_{size}.bin"
            for dc in range(48, 69)
            for size in [
                "100.0K",
                "300.0K",
                "600.0K",
                "1.0M",
            ]
        ]
        + [
            f"{SAMPLE_DIR}/75deg/{size}/75degT_dc{dc}_{size}.bin"
            for dc in range(48, 69)
            for size in [
                "100.0K",
                "300.0K",
                "600.0K",
                "1.0M",
            ]
        ]
    )
    return files


def main():
    test_names = [
        "most_common_value_test",
        "collision_test",
        "markov_test",
        "compression_test",
        "t_tuple_test",
        "lrs_test",
        "multi_mcw_test",
        "lag_prediction_test",
        "multi_markov_test",
        "lz78y_test",
    ]
    results = {}
    record = []
    # Seeding dictionary
    for test_name in test_names:
        results[test_name] = 0
    for filename in gen_files():
        print(f"Testing {filename}")
        Hs = []
        for test_name in test_names:
            with Popen(
                ["ea_non_iid", "-T", test_name, filename], stdout=PIPE, stdin=PIPE
            ) as process:
                stdout, _stderr = process.communicate()
                lines = stdout.decode("utf-8").split("\n")
                lines = lines[-4:-1]
                vals = [float(line.split(" ")[-1]) for line in lines if len(line) > 2]
                h = np.min([vals[0], 8 * vals[1]])
                print(f"{test_name}: {h}")
                Hs.append(h)
        best = test_names[np.argmin(Hs)]
        results[best] += 1
        record.append((filename, best))
    print(record)
    print(results)


if __name__ == "__main__":
    main()
