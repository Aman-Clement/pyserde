"""
yamlfile.py

Read swagger echo example yaml.

Usage:
    $ poetry install
    $ poetry run python yamlfile.py
"""

from typing import Optional, Union
import pathlib

from serde import Untagged, serde
from serde.yaml import from_yaml

basedir = pathlib.Path(__file__).parent


@serde(rename_all="camelcase")
class Info:
    title: str
    description: str
    version: str


@serde(rename_all="camelcase")
class Parameter:
    name: str
    # not yet supported.
    # infield: str = field(rename='in')
    type: str
    required: bool


@serde(rename_all="camelcase")
class Response:
    description: str


@serde(rename_all="camelcase", tagging=Untagged)
class Path:
    description: str
    operation_id: str
    parameters: list[Union[str, Parameter]]
    responses: dict[Union[str, int], Response]


@serde(rename_all="camelcase")
class Prop:
    type: str
    format: Optional[str]


@serde(rename_all="camelcase")
class Definition:
    required: Optional[list[str]]
    properties: dict[str, Prop]


@serde(rename_all="camelcase")
class Swagger:
    swagger: int
    info: Info
    host: str
    schemes: list[str]
    base_path = str
    produces: list[str]
    paths: dict[str, dict[str, Path]]
    definitions: dict[str, Definition]


def main() -> None:
    with open(basedir / "swagger.yml") as f:
        yaml = f.read()
    swagger = from_yaml(Swagger, yaml)
    print(swagger)


if __name__ == "__main__":
    main()
