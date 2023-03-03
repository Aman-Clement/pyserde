from dataclasses import dataclass

from serde import serde
from serde.msgpack import from_msgpack, to_msgpack


@serde
@dataclass
class Foo:
    i: int
    s: str
    f: float
    b: bool


def main():
    f = Foo(i=10, s='foo', f=100.0, b=True)
    p = to_msgpack(f)
    print(f"Into MsgPack: {p}")
    print(f"From MsgPack: {from_msgpack(Foo, p)}")


if __name__ == '__main__':
    main()
