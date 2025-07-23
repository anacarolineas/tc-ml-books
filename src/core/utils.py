from typing import Iterator
from pydantic import BaseModel

def format_as_json_lines_training_data(data_stream: Iterator[BaseModel]) -> Iterator[str]:
    """
    A generator that formats each item in the stream as a JSON line.
    """
    yield '['
    first = True
    for item in data_stream:
        if not first:
            yield ','
        yield item.model_dump_json()
        first = False
    yield ']'