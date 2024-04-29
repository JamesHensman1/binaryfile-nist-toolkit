from subprocess import Popen, PIPE
import timeit

PROJECT_DIR = '/home/james/Desktop/Project' #Change me
filename = "{PROJECT_DIR}/Reshaped/AmbientT_dc60raw.bin"

def run(test_name):
    start_time = timeit.default_timer()
    with Popen(
        ["ea_non_iid", "-T", test_name, filename], stdout=PIPE, stdin=PIPE
    ) as process:
        stdout, _stderr = process.communicate()
        end_time = timeit.default_timer()
        print(f"Execution time ({test_name}): {end_time - start_time} seconds")


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

for test in test_names:
    run(test)
