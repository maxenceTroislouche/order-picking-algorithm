import os
import shutil
import subprocess
import time
from pathlib import Path

CHECKER_DIR = Path('../checker')


class CheckerError(Exception):
    pass


def _copy_files(instance_file: Path, solution_file: Path):
    instance_destination = CHECKER_DIR / 'instance.txt'
    solution_destination = CHECKER_DIR / 'instance_sol.txt'

    # Remove old files if they exist
    instance_destination.unlink(missing_ok=True)
    solution_destination.unlink(missing_ok=True)

    # Copy instance and solution files to checker directory
    shutil.copyfile(instance_file, instance_destination)
    shutil.copyfile(solution_file, solution_destination)


def _parse_stdout(stdout: str) -> tuple[int, int, float]:
    lines = stdout.split('\n')

    number_of_trolleys = None
    number_of_boxes = None
    total_distance = None

    for line in lines:
        if "tournees" in line:
            number_of_trolleys = int(line.split(":")[1])
        elif "colis" in line:
            number_of_boxes = int(line.split(":")[1])
        elif "Distance" in line:
            total_distance = float(
                line.split(":")[1]
                    .split("m")[0]
                    .replace(',', '.')
                    .replace(' ', '')
                )

    if None in (number_of_trolleys, number_of_boxes, total_distance):
        return -1, -1, -1

    return number_of_trolleys, number_of_boxes, total_distance


def get_checker_data(instance_file: Path, solution_file: Path) -> tuple[int, int, float]:
    """
    Run the checker on the instance and solution files and return the results.
    :param instance_file: Path to the instance file
    :param solution_file: Path to the solution file
    :return: Tuple containing the number of trolleys, the number of boxes, and the total distance
    """
    # Copy files to checker directory
    _copy_files(instance_file, solution_file)

    # Run checker
    command = ['java', '-jar', '../checker/CheckerBatchingPicking.jar', '../checker/instance']

    print(f"Executing command : {' '.join(command)}")

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    stdout, stderr = process.communicate()

    print(stdout)

    if "FAILED" in stdout:
        return -1, -1, -1
        # raise CheckerError(f'Checker failed with error: {stderr}')

    # Parse checker output
    number_of_trolleys, number_of_boxes, total_distance = _parse_stdout(stdout)

    print(f"Checker results: {number_of_trolleys=}, {number_of_boxes=}, {total_distance=}")
    return number_of_trolleys, number_of_boxes, total_distance


def write_results(checker_data: list[tuple[Path, Path, int, int, float]], result_path: Path):
    """
    Write the checker results to a CSV file.
    :param checker_data: List of tuples containing the instance file, solution file, number of trolleys, number of boxes
    , and total distance
    :param result_path: Path to the result file
    """
    with open(result_path, 'w') as f:
        f.write('instance_file,solution_file,number_of_trolleys,number_of_boxes,total_distance\n')
        for instance_file, solution_file, number_of_trolleys, number_of_boxes, total_distance in checker_data:
            f.write(f'{instance_file},{solution_file},{number_of_trolleys},{number_of_boxes},{total_distance}\n')
