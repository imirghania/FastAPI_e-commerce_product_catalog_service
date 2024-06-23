import sys
from importlib import import_module
from inspect import isclass
from pathlib import Path
from typing import Iterator
from beanie import Document


FILE_PATH = Path(__file__)

APP_DIR = FILE_PATH.parent.parent


def is_beanie_model(item) -> bool:
    """Determines if item is a Beanie Document object."""
    return (isclass(item) and issubclass(item, Document) )


def get_modules(module) -> Iterator[str]:
    """Returns all .py modules in given file_dir as
    a generator of dot separated string values.
    """
    file_dir = Path(APP_DIR/module)
    idx_app_root = len(APP_DIR.parts) - 1
    modules = [f for f in list(file_dir.rglob("*.py")) 
                if f.stem != "__init__"]
    for filepath in modules:
        yield (".".join(filepath.parts[idx_app_root:])[0:-3])


def dynamic_loader(module, compare) -> list:
    """Iterates over all .py files in `module` directory,
    finding all classes that match `compare` function.
    """
    items = []
    for mod in get_modules(module):
        module = import_module(mod)
        if hasattr(module, "__all__"):
            objs = ([getattr(module, obj)
                    for obj in module.__all__])
            items += [o for o in objs
                    if compare(o) and o not in items]
    return items


def get_beanie_models() -> list[str]:
    """Dynamic Beanie model finder."""
    sys.path.append(APP_DIR)
    # return dynamic_loader("fastapi_pcatalog_service.models", is_beanie_model)
    return dynamic_loader("models", is_beanie_model)


# def db_models() -> list[str]:
#     """Create a list of Beanie models to include in db initialization."""
#     objs = get_beanie_models()

#     obj_list = [f"{o.__module__}.{o.__name__}" for o in objs]

#     return obj_list


if __name__ == "__main__":
    print(APP_DIR)
    sys.path.append(APP_DIR)
    print(dynamic_loader("models", is_beanie_model))
    # print(list(get_modules('models')))