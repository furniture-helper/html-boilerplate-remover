from src.boilerplate_remover.BoilerplateRemover import BoilerplateRemover
from src.boilerplate_remover.utils.file_utils import write_string_to_file

boilerplate_remover = BoilerplateRemover()

minimized_tree = boilerplate_remover.get_minimized_tree(
    "data/https___www_singersl_com_product_samsung_refrigerator_rt40h28wnqig_253l_inverter.html")
print(minimized_tree)

write_string_to_file("output/test.html", minimized_tree.to_html())
