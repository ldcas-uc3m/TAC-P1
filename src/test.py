import subprocess
from pathlib import Path
import json
import platform
import logging

import matplotlib as plt
import pandas as pd

import jf2tm


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(handler)


REPO_ROOT = Path(__file__).parent.parent
TURING_EXEC: Path = REPO_ROOT / f"turing-machine-simulator/turing{'.exe' if platform.system() == 'Windows' else ''}"
DATA_FOLDER = REPO_ROOT / "data/"


def tests(file: Path, inputs: list[str], ntapes: int = 0) -> pd.DataFrame:
    """
    Runs the specified `inputs` through the Turing Machine in `file`, on the Turing Machine simulator in `TURING_EXEC`, and returns the results.

    :param file: Turing machine definition file path, in turingmachinesimulator.com format.
    :param inputs: List of inputs to the TM.
    :param ntapes: Number of tapes of the TM.

    :return: DataFrame with columns {n, steps, result}
    """

    results = pd.DataFrame(
        columns=[
            'input',
            'n',
            'steps',
            *[f'result{i}' for i in range(ntapes)]
        ]
    )

    for input in inputs:
        tm_result = json.loads(subprocess.check_output([TURING_EXEC, str(file), input, "--json"]))

        if not tm_result["accepted"]:
            logger.error(f"Input '{input}' for TM {file} was not accepted")
            continue

        r = {
            'input': input,
            'n': len(input),
            'steps': tm_result["steps"],
            **{f'result{i}': tm_result["tapes"][i].strip("_") for i in range(ntapes)}
        }


        # append to results
        results.loc[len(results)] = r


    return results




def plot_scatter_from_csv(csv_file, x_column, y_column, save_file=None):
   
    # Cargar los datos del archivo CSV en un DataFrame
    df = pd.read_csv(csv_file)

    # Extraer las columnas x e y del DataFrame
    x = df[x_column]
    y = df[y_column]

    # Crear el gráfico 
    plt.scatter(x, y, color='blue', label='Puntos de datos')

    # Agregar etiquetas y título
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.title('Gráfico de dispersión de {} y {}'.format(x_column, y_column))

    plt.legend()

    if save_file:
        plt.savefig(save_file)

    plt.show()
    
    



if __name__ == "__main__":
    if not TURING_EXEC.exists():
        exit(f"TM simulator executable not found at {TURING_EXEC}. Have you run make?")


    jff_files = [
        REPO_ROOT / "src/MT-0A.jff",
        REPO_ROOT / "src/MT-0B.jff",
        # REPO_ROOT / "src/MT-0C.jff",  # non-deterministic, cannot test
        REPO_ROOT / "src/MT-1A.jff",
        REPO_ROOT / "src/MT-1B.jff",
        REPO_ROOT / "src/MT-2A.jff"
    ]

    for machine_file in jff_files:
        machine_name = ".".join(machine_file.name.split(".")[:-1])

        # convert & save to file
        tm_file = Path(f"{machine_file.parent}/{machine_name}.tm")
        with open(tm_file, "+wt") as fd:
            fd.write(jf2tm.convert(machine_file, machine_name))

        # run tests

        match machine_name:
            case "MT-0A" | "MT-0B":
                inputs = [
                    "",
                    "aa",
                    "abba",
                    "abaaba",
                    "aaabbaaa",
                    "bbaabbaabb",
                    "bbbbbaabbbbb"
                ]

            case "MT-1A":
                inputs = [
                    "$1",
                    "$11",
                    "$111",
                    "$1111",
                    "$11111"
                ]

            case "MT-1B":
                inputs = [
                    "1$1",
                    "1$11",
                    "1$111",
                    "1$1111",
                ]

            case _:
                logger.warning(f"There are no predefined inputs for {machine_name}!")
                continue

        tapes = 2 if machine_name.endswith("B") else 1

        logger.info(f"Performing tests for {machine_name}...")
        df = tests(tm_file, inputs, ntapes=tapes)

        # save results
        logger.info(f"Saving results to {DATA_FOLDER / f'{machine_name}.csv'}...")
        df.to_csv(DATA_FOLDER / f'{machine_name}.csv', index=False)