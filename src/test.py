import subprocess
from pathlib import Path
import json

import pandas as pd

import jf2txt


REPO_ROOT = Path(__file__).parent.parent
TURING_EXEC: Path = REPO_ROOT / "turing-machine-simulator/turing"
DATA_FOLDER = REPO_ROOT / "data/"



def tests(file: Path, inputs: list[str]) -> pd.DataFrame:
    """
    Runs the specified `inputs` through the Turing Machine in `file`, on the Turing Machine simulator in `TURING_EXEC`, and returns the results.

    :param file: Turing machine definition file path, in turingmachinesimulator.com format.
    :param inputs: List of inputs to the TM.

    :return: DataFrame with columns {n, steps, result}
    """

    results = pd.DataFrame(columns=['n', 'steps', 'result'])

    for i in inputs:
        tm_result = json.loads(subprocess.check_output([TURING_EXEC, str(file), i, "--json"]))

        if not tm_result["accepted"]:
            print(f"ERROR: Input {i} for TM {file} was not accepted")
            continue

        r = {
            'n': len(i),
            'steps': tm_result["steps"],
            'result': tm_result["final_word"].strip("_")
        }

        # append to results
        results.loc[len(results)] = r


    return results



if __name__ == "__main__":
    if not TURING_EXEC.exists():
        exit(f"TM simulator executable not found at {TURING_EXEC}. Have you run make?")


    jff_files = [
        REPO_ROOT / "src/MT-0A.jff",
        REPO_ROOT / "src/MT-0B.jff"
    ]

    for machine_file in jff_files:
        machine_name = ".".join(machine_file.name.split(".")[:-1])

        # convert & save to file
        output = Path(f"{machine_file.parent}/{machine_name}.tm")
        with open(output, "+wt") as fd:
            fd.write(jf2txt.convert(machine_file, machine_name))

        # run tests
        df = tests(output, ["abba", "babababa", "aaaaaaaa"])

        # save results
        df.to_csv(DATA_FOLDER / f"{machine_name}.csv")
