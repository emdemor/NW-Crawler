from importlib import resources


def run():
    filepath = str(
        resources.files("sample.submodule.assets").joinpath("submodule_file.txt")
    )

    with open(filepath, "r") as file:
        content = file.read()

    print(content)
