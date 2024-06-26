import subprocess
from pathlib import Path
import json
import os
import platform
import logging
from typing import Callable
from itertools import product

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors

import jf2tm



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(handler)


REPO_ROOT = Path(__file__).parent.parent
TURING_EXEC: Path = REPO_ROOT/f"turing-machine-simulator/turing{'.exe' if platform.system() == 'Windows' else ''}"
DATA_FOLDER = REPO_ROOT/"data/"
TM_FOLDER = REPO_ROOT/"src/tm/"

if os.path.exists(REPO_ROOT/"report"):
    IMAGE_FOLDER = REPO_ROOT/"report/img/"
else:
    IMAGE_FOLDER = DATA_FOLDER/"img"
    os.mkdir(IMAGE_FOLDER)




# ==============
# TEST FUNCTIONS
# ==============

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



# ==============
# PLOT FUNCTIONS
# ==============


def plot_dataframes(
    dfs: dict[str, pd.DataFrame],
    x_column: str,
    y_column: str,
    save_file: str | None = None
):
    """
    Plots dataframes.

    :param df: Map of DF name and DF.
    :param x_column: Column from DF to represent on the X axis.
    :param y_column: Column from DF to represent on the Y axis.
    :param save_file: File to save the image to. If `None`, shows the plot.
    """

    # Crear el gráfico
    fig, ax = plt.subplots()

    for name, df in dfs.items():
        ax.plot(df[x_column], df[y_column], marker='o', label=name)

    # automatic colors
    if len(dfs) <= len(mcolors.BASE_COLORS):
        pallete = mcolors.BASE_COLORS
    else:
        pallete = mcolors.XKCD_COLORS

    ax.set_prop_cycle(color=pallete)

    # Agregar etiquetas
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)

    ax.legend()

    if save_file:
        fig.savefig(save_file)
    else:
        fig.show()

    plt.close()



def plot_functions(
    funcs: dict[str, Callable[[np.ndarray], np.ndarray]],
    n0: int = 10,
    n_max: int = 100,
    granularity: int = 1,
    save_file: str | Path | None = None
):
    """
    Plots functions refering to the complexity of turing machines (in terms of n and number of steps).

    :param funcs: Map of function name and function (`{"f(n)": f_n, ...}`).
    :param n0: Initial value of n.
    :param n_max: Maximum value of n to plot.
    :param granularity: Granularity of the plot. Default (`1`) means plot `nmax - n0` random points
    :param save_file: File to save the image to. If `None`, shows the plot.
    """

    fig, ax = plt.subplots()

    x = np.linspace(n0, n_max, granularity * (n_max - n0))

    for name, fn in funcs.items():
        ax.plot(x, fn(x), label=name)

    # automatic colors
    if len(funcs) <= len(mcolors.BASE_COLORS):
        pallete = mcolors.BASE_COLORS
    else:
        pallete = mcolors.XKCD_COLORS

    ax.set_prop_cycle(color=pallete)

    # Agregar etiquetas
    ax.set_xlabel('n')
    ax.set_ylabel('steps')

    ax.legend()

    if save_file:
        fig.savefig(save_file)
    else:
        fig.show()

    plt.close()



def plot_complexity(
    func: Callable[[np.ndarray], np.ndarray],
    data: pd.DataFrame,
    x_column: str,
    y_column: str,
    save_file: str | Path | None = None
):
    """
    Plots the complexity of a function, relating real data and theoretical (in terms of n and number of steps).

    :param funcs: Map of function name and function (`{"f(n)": f_n, ...}`).
    :param x_column: Column from DF to represent on the X axis.
    :param y_column: Column from DF to represent on the Y axis.
    :param save_file: File to save the image to. If `None`, shows the plot.
    """

    n0 = data[x_column].iloc[0]
    nmax = data[x_column].iloc[-1]


    fig, ax = plt.subplots()

    x = np.linspace(n0, nmax, nmax - n0)

    # function
    ax.plot(x, func(x), label="T(n) (aprox.)", color="red")

    # dataframe
    ax.plot(data[x_column], data[y_column], label="T(n)", marker='o', color='blue')

    # Agregar etiquetas
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)

    ax.legend()

    if save_file:
        fig.savefig(save_file)
    else:
        fig.show()

    plt.close()



if __name__ == "__main__":
    if not TURING_EXEC.exists():
        exit(f"TM simulator executable not found at {TURING_EXEC}. Have you run make?")


    jff_files = [
        TM_FOLDER / "MT-0A.jff",
        TM_FOLDER / "MT-0B.jff",
        TM_FOLDER / "MT-1A.jff",
        TM_FOLDER / "MT-1B.jff",
        TM_FOLDER / "MT-2A.jff",
        TM_FOLDER / "MT-2B.jff",
        TM_FOLDER / "MT-4A.jff",
        TM_FOLDER / "MT-5A.jff",
        TM_FOLDER / "MT2T-6A.jff",
        TM_FOLDER / "MT3T-6A.jff",
        TM_FOLDER / "MT-7B.jff"
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
                ntapes = 2 if machine_name.endswith("B") else 1

            case "MT-1A":
                inputs1 = [f"${'1'*i}" for i in range(1,6)]
                inputs2 = [
                    "1$1",
                    "11$111",
                    "1111$11111",
                    "111111$1111111111",
                    "11111111111111$111111111111111111111" 
                    ]
                inputs = inputs1+inputs2
                ntapes = 1

            case "MT-1B":
                inputs1 = [f"{'1'*i}$" for i in range(1,6)]
                inputs2 = [
                    "1$1",
                    "111$11",
                    "11111$1111",
                    "1111111111$111111",
                    "111111111111111111111$11111111111111" 
                    ]
                inputs = inputs1+inputs2
                ntapes = 2

            case "MT-2A":
                inputs1 = [f"1${'1'*i}" for i in range(1,7)]
                inputs2 = [
                    "1$1",
                    "10$11",
                    "100$101",
                    "110$1010",
                    "1110$10101"
                ] 
                inputs = inputs1+inputs2
                ntapes = 1

            case "MT-2B":
                inputs1 = [f"1${'1'*i}" for i in range(1,7)]
                inputs2 = [
                    "1$1",
                    "10$11",
                    "100$101",
                    "110$1010",
                    "1110$10101"
                ] 
                inputs = inputs1+inputs2

            case "MT-4A":
                inputs = [
                    "2$2",
                    "2$22",
                    "2$222",
                    "2$2222",
                    "2$22222",
                    "2$222222",
                    "1$1",
                    "2$10",
                    "11$12",
                    "20$101",
                    "112$210"
                ]

            case "MT-5A" | "MT2T-6A" | "MT3T-6A":
                inputs = ["a"*3*i for i in range(1, 5)]
                ntapes = 3 if "3" in machine_name else 2

            case "MT-7B":
                inputs = [
                    "11",
                    "111",
                    "11111",
                    "1111111",
                    "11111111111"
                ]
                ntapes = 2

            case _:
                logger.warning(f"There are no predefined inputs for {machine_name}!")
                continue


        logger.info(f"Performing tests for {machine_name}...")
        df = tests(tm_file, inputs, ntapes=ntapes)

        # save results
        logger.debug(f"Saving results to {DATA_FOLDER / f'{machine_name}.csv'}...")
        df.to_csv(DATA_FOLDER / f'{machine_name}.csv', index=False)

        # plot results
        plot_dataframes({machine_name: df}, 'n', 'steps', IMAGE_FOLDER / f"plot_{machine_name}_results.svg")


    # plot complexity
    logger.info("Plotting complexity functions...")

    COMPLEXITY_FUNCTIONS = {
        'MT-0A': {
            'T(n)': lambda n : 2*n**2 + 6*n + 2,
            'O(n)': lambda n : (131/50)*n**2
        },
        'MT-0B': {
            'T(n)': lambda n : 3*n + 3,
            'O(n)': lambda n : (33/10)*n
        },
        'MT-0C': {
            'T(n)': lambda n : n + 2,
            'O(n)': lambda n : (12/10)*n
        },
        'MT-1A': {
            'T(n)': lambda n : 2*n**2 + 5*n + 4,
            'O(n)': lambda n : (127/50)*n**2
        },
        'MT-1B': {
            'T(n)': lambda n : 2*n - 2,
            'O(n)': lambda n : 2*n
        },
        'MT-2A': {
            'T(n)': lambda n : 16*n**2 - 55*n + 63,
            'O(n)': lambda n : (1663/100)*n**2
        },
        'MT-5A': {
            'T(n)': lambda n : 2*n + 4,
            'O(n)': lambda n : (12/5)*n
        },
        'MT-5B': {
            'T(n)': lambda n : n + 2,
            'O(n)': lambda n : (6/5)*n
        },
        'MT2T-6A': {
            'T(n)': lambda n : (8/3)*n + 6,
            'O(n)': lambda n : (49/15)*n
        },
        'MT3T-6A': {
            'T(n)': lambda n : (7/3)*n + 5,
            'O(n)': lambda n : (17/6)*n
        },
        'MT2T-6B': {
            'T(n)': lambda n : (5/3)*n + 5,
            'O(n)': lambda n : (31/15)*n
        },
        'MT3T-6B': {
            'T(n)': lambda n : (4/3)*n + 3,
            'O(n)': lambda n : (49/30)*n
        },
        'MT-7A': {
            'T(n)': lambda n : (3/2)*n + 3
        },
        'MT-7B': {
            'T(n)': lambda n : (13/6)*n**2 + (7/6)*n -5
        }
    }

    for machine_name, funcs in COMPLEXITY_FUNCTIONS.items():
        if len(funcs) == 1:  # plot T(n) vs empirical results
            plot_complexity(
                COMPLEXITY_FUNCTIONS[machine_name]['T(n)'],
                pd.read_csv(DATA_FOLDER/f"{machine_name}.csv"),
                x_column='n',
                y_column='steps',
                save_file=IMAGE_FOLDER/f"plot_{machine_name}_complexity.svg"
            )
        else:  # plot T(n) vs O(n)
            plot_functions(funcs, save_file=IMAGE_FOLDER/f"plot_{machine_name}_complexity.svg")


    logger.info("Plotting comparisons...")

    # plot comparison 1 VS 2, one tape
    df1 = pd.DataFrame({'steps': [15, 53, 127, 386, 1607], 'n': [2, 5, 9, 16, 35]})
    df2 = pd.DataFrame({'steps': [21, 47, 83, 172, 372], 'n': [2, 5, 9, 16, 35]})
    plot_dataframes({'Base 1': df1, 'Base 2': df2}, 'n', 'steps', IMAGE_FOLDER / f"plot_comparative1&2_1tape.svg")

    # plot comparison 1 VS 2, two tape
    df1 = pd.DataFrame({'steps': [5, 10, 16, 28, 58], 'n': [2, 5, 9, 16, 35]})
    df2 = pd.DataFrame({'steps': [17, 50, 93, 204, 507], 'n': [2, 5, 9, 16, 35]})
    plot_dataframes({'Base 1': df1, 'Base 2': df2}, 'n', 'steps', IMAGE_FOLDER / f"plot_comparative1&2_2tape.svg")

    # plot comparison 1 VS 3, two tape
    df1 = pd.DataFrame({'steps': [5, 10, 16, 28, 58], 'n': [2, 5, 9, 16, 35]})
    df2 = pd.DataFrame({'steps': [15, 43, 75, 162, 384], 'n': [2, 5, 9, 16, 35]})
    plot_dataframes({'Base 2': df1, 'Base 3': df2}, 'n', 'steps', IMAGE_FOLDER / f"plot_comparative1&3_2tape.svg")

    # plot comparison 2 VS 3, two tape
    df1 = pd.DataFrame({'steps': [17, 50, 93, 204, 507], 'n': [2, 5, 9, 16, 35]})
    df2 = pd.DataFrame({'steps': [15, 43, 75, 162, 384], 'n': [2, 5, 9, 16, 35]})
    plot_dataframes({'Base 2': df1, 'Base 3': df2} , 'n', 'steps', IMAGE_FOLDER / f"plot_comparative2&3_2tape.svg")


    # comparing T(n) between machines
    machine_comparisons: dict[str, list[list[str]]] = {
        **{f"MT-6{x}": [f"MT{n}T-6{x}" for n in (2, 3)] for x in ("A", "B")},  # MT-6A & MT-6B, 2T vs 3T
        "MT-6": [f"MT{n}T-6{x}" for n, x in product([2, 3], ["A", "B"])],  # all MT-6
        'MT-7': ['MT-7A', 'MT-7B']
    }

    for name, machines in machine_comparisons.items():
        plot_functions(
            {machine: COMPLEXITY_FUNCTIONS[machine]['T(n)'] for machine in machines},
            save_file=IMAGE_FOLDER / f"plot_{name}_comparison.svg",
            n0=3,
            n_max=40
        )

    # plot all
    plot_functions(
        {name: functions['T(n)'] for name, functions in COMPLEXITY_FUNCTIONS.items() if "T(n)" in functions},
        save_file=IMAGE_FOLDER / "plot_all_complexity.svg",
        n0=1,
        granularity=10,
        n_max=6
    )

