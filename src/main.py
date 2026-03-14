from pathlib import Path

from src.boilerplate_remover.BoilerplateRemover import BoilerplateRemover
from src.boilerplate_remover.utils.file_utils import write_string_to_file

boilerplate_remover = BoilerplateRemover(cache_path=".cache/anchor_tree.pkl")


# minimized_tree = boilerplate_remover.get_minimized_tree(
#     "data/https___www_singersl_com_product_samsung_refrigerator_rt40h28wnqig_253l_inverter.html")
# print(minimized_tree)
#
# write_string_to_file("output/test.html", minimized_tree.to_html())

def process_data_dir(data_dir: str = "data", output_dir: str = "output") -> None:
    """
    For each .html/.htm file in `data_dir`, get minimized tree and write HTML to `output_dir`.
    """
    data_path = Path(data_dir)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    exts = {".html", ".htm"}

    for file in sorted(data_path.iterdir()):
        if not file.is_file() or file.suffix.lower() not in exts:
            continue

        try:
            minimized = boilerplate_remover.get_minimized_tree(str(file))
            target = out_path / file.name
            write_string_to_file(str(target), minimized.to_html())
            print(f"Wrote: `{target}`")
        except Exception as e:
            print(f"Failed `{file}`: {e}")


process_data_dir()


def get_total_file_size(dir_path: str = "data") -> int:
    total_size = 0
    for file in Path(dir_path).iterdir():
        if file.is_file():
            total_size += file.stat().st_size
    return total_size


input_size = get_total_file_size("data")
output_size = get_total_file_size("output")

print(f"Total input size:\t {input_size} bytes")
print(f"Total output size:\t {output_size} bytes")

percentage_reduction = ((input_size - output_size) / input_size) * 100 if input_size > 0 else 0
print(f"Percentage reduction:\t {percentage_reduction:.2f}%")
