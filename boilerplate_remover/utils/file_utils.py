import os


def read_file_to_string(file_path) -> str:
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        return file.read()


def write_string_to_file(file_path: str, content: str) -> None:
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def get_all_files_in_directory(directory_path: str) -> list[str]:
    all_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files
