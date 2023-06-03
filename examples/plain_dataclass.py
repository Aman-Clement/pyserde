from dataclasses import dataclass

from serde.json import from_json, to_json


# Works without @serde since v0.10.0
@dataclass
class Foo:
    i: int
    s: str
    f: float
    b: bool


def main() -> None:
    f = Foo(i=10, s="foo", f=100.0, b=True)
    print(f"Into Json: {to_json(f)}")

    s = '{"i": 10, "s": "foo", "f": 100.0, "b": true}'
    print(f"From Json: {from_json(Foo, s)}")


if __name__ == "__main__":
    main()
