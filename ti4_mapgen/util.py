from typing import TypeVar

from dataclass_wizard import Container

T = TypeVar("T")


def get_dataclasses_from_file(obj: type[T], file: str) -> Container[T]:
    return Container[obj](obj.from_json_file(file))


def filter_dataclasses(obj: type[T], dataclasses: list[T], args: dict[str, list[str]]) -> Container[T]:
    results = Container[obj](dataclasses)
    for key, values in args.items():
        if key in obj.__annotations__.keys():
            if obj.__annotations__[key] == int:
                values = [int(value) for value in values]
            results = Container[obj]([item for item in results if getattr(item, key) in values])

    return results
