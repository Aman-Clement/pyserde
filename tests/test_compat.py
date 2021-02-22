import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

import pytest

from serde.compat import is_dict, is_list, is_opt, is_tuple, is_union, iter_types, type_args, union_args
from serde.core import is_instance

from .data import Bool, Float, Int, Pri, PriOpt, Str


def test_types():
    assert is_list(List[int])
    assert is_list(List)
    assert is_tuple(Tuple[int, int, int])
    assert is_tuple(Tuple)
    assert is_dict(Dict[str, int])
    assert is_dict(Dict)
    assert is_opt(Optional[int])
    assert is_union(Union[int, str])
    assert is_union(Union[Optional[int], Optional[str]])
    assert is_opt(Optional[int])
    assert not is_union(Optional[int])
    assert not is_opt(Union[Optional[int], Optional[str]])
    assert is_union(Union[Optional[int], Optional[str]])

    if sys.version_info[:3] >= (3, 9, 0):
        assert is_list(list[int])
        assert is_list(list)
        assert is_tuple(tuple[int, int, int])
        assert is_tuple(tuple)
        assert is_dict(dict[str, int])
        assert is_dict(dict)


def test_iter_types():
    assert [Pri, int, str, float, bool] == list(iter_types(Pri))
    assert [str, Pri, int, str, float, bool] == list(iter_types(Dict[str, Pri]))
    assert [str] == list(iter_types(List[str]))
    assert [int, str, bool, float] == list(iter_types(Tuple[int, str, bool, float]))
    assert [PriOpt, int, str, float, bool] == list(iter_types(PriOpt))


def test_type_args():
    assert (int,) == type_args(List[int])
    assert (int, str) == type_args(Dict[int, str])
    assert (int, type(None)) == type_args(Optional[int])
    assert (Optional[int],) == type_args(List[Optional[int]])
    assert (List[int], type(None)) == type_args(Optional[List[int]])
    assert (List[int], Dict[str, int]) == type_args(Union[List[int], Dict[str, int]])
    assert (int, type(None), str) == type_args(Union[Optional[int], str])

    if sys.version_info[:3] >= (3, 9, 0):
        assert (int,) == type_args(list[int])
        assert (int, str) == type_args(dict[int, str])
        assert (int, str) == type_args(tuple[int, str])


def test_union_args():
    assert (int, str) == union_args(Union[int, str])
    assert (List[int], Dict[int, str]) == union_args(Union[List[int], Dict[int, str]])
    assert (Optional[int], str) == union_args(Union[Optional[int], str])


def test_is_instance():
    # Primitive
    assert is_instance(10, int)
    assert is_instance("str", str)
    assert is_instance(1.0, float)
    assert is_instance(False, bool)
    assert not is_instance(10.0, int)
    assert not is_instance("10", int)
    assert is_instance(True, int)  # see why this is true https://stackoverflow.com/a/37888668

    # Dataclass
    p = Pri(i=10, s='foo', f=100.0, b=True)
    assert is_instance(p, Pri)
    p.i = 10.0
    # for speed reasons we do not detect wrong types within dataclasses
    assert is_instance(p, Pri)

    # Dataclass (Nested)
    @dataclass
    class Foo:
        p: Pri

    h = Foo(Pri(i=10, s='foo', f=100.0, b=True))
    assert is_instance(h, Foo)
    h.p.i = 10.0
    # for speed reasons we do not detect wrong types within dataclasses
    assert is_instance(h, Foo)

    # List
    assert is_instance([], List[int])
    assert is_instance([10], List)
    assert is_instance([10], list)
    assert is_instance([10], List[int])
    assert not is_instance([10.0], List[int])

    # List of dataclasses
    assert is_instance([Int(n) for n in range(1, 10)], List[Int])
    assert not is_instance([Str("foo")], List[Int])

    # Tuple
    assert is_instance(tuple(), Tuple[int, str, float, bool])
    assert is_instance((10,"a"), Tuple)
    assert is_instance((10,"a"), tuple)
    assert is_instance((10, 'foo', 100.0, True), Tuple[int, str, float, bool])
    assert not is_instance((10, 'foo', 100.0, "last-type-is-wrong"), Tuple[int, str, float, bool])

    # Tuple of dataclasses
    assert is_instance((Int(10), Str('foo'), Float(100.0), Bool(True)), Tuple[Int, Str, Float, Bool])
    assert not is_instance((Int(10), Str('foo'), Str("wrong-class"), Bool(True)), Tuple[Int, Str, Float, Bool])

    # Dict
    assert is_instance({}, Dict[str, int])
    assert is_instance({"a":"b"}, Dict)
    assert is_instance({"a":"b"}, dict)
    assert is_instance(dict(foo=10, bar=20), Dict[str, int])
    assert not is_instance(dict(foo=10.0, bar=20), Dict[str, int])

    # Dict of dataclasses
    assert is_instance({Str('foo'): Int(10), Str('bar'): Int(20)}, Dict[Str, Int])
    assert not is_instance({Str('foo'): Str('wrong-type'), Str('bar'): Int(10)}, Dict[Str, Int])

    # Optional
    assert is_instance(None, type(None))
    assert is_instance(10, Optional[int])
    assert is_instance(None, Optional[int])
    assert not is_instance("wrong-type", Optional[int])

    # Optional of dataclass
    assert is_instance(Int(10), Optional[Int])
    assert not is_instance("wrong-type", Optional[Int])

    # Nested containers
    assert is_instance([({"a":"b"}, 10, [True])], List[Tuple[Dict[str,str],int,List[bool]]])
    assert not is_instance([({"a":"b"}, 10, ["wrong-type"])], List[Tuple[Dict[str,str],int,List[bool]]])
