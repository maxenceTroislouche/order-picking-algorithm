from pathlib import Path


def get_instance_files(instance_directory: Path) -> list[Path]:
    instances = []
    for file in Path(instance_directory).iterdir():
        if file.is_file():
            instances.append(file)

    return instances


def get_solution_file_path(solution_directory: Path, instance_file_path: Path) -> Path:
    return Path(solution_directory, instance_file_path.stem + '_sol.txt')
