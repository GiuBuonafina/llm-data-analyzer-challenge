
def load_resource(path):
    """
    Responsável por carregar o conteúdo de um arquivo de texto, como o sintax.txt e o data_dictionary.txt
    """
    with open(path, encoding="utf-8") as f:
        return f.read()