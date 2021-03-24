from typing import Union


def cast(value: str) -> Union[str, float, int]:
    """Try to cast str to the corresponding value"""
    try:
        if '.' in value:
            return float(value)

        return int(value)

    except ValueError:
        pass

    return value
