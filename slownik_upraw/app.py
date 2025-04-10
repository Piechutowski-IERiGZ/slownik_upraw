import itertools as it
import sqlite3 as s3
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


from litestar import Litestar, MediaType, get
from litestar.types import ControllerRouterHandler
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import create_static_files_router
from litestar.template import TemplateConfig
from litestar.response import Template

from slownik_upraw.db import run_fixture, connection, close_connection


HTML_MEDIA: str = MediaType.HTML


@dataclass
class Uprawa:
    IdUPrawy: str
    Nazwa: str
    NazwaLacinska: str
    Opis: str

@dataclass
class Gatunek:
    IdGatunek: str
    Nazwa: str
    Uprawy: list[Uprawa]

@dataclass
class Kategoria:
    IdKategoria: str
    Nazwa: str
    Gatunki: list[Gatunek]


lista_kategorii = []
for x in range(1, 4):
    lista_gatunek = []
    for y in range(1, 5):
        lista_upraw = []
        for z in range(1, 6):
            lista_upraw.append(Uprawa(
                IdUPrawy=f"01.{x:02d}.{y:02d}.{z:02d}",
                Nazwa=f"Uprawa 01.{x:02d}.{y:02d}.{z:02d}",
                NazwaLacinska=f"Uprawa Latina 01.{x:02d}.{y:02d}.{z:02d}",
                Opis="Lorem ipsum dolor sit amet consectetur adipiscing elit.",
            ))
        lista_gatunek.append(Gatunek(
            IdGatunek=f"01.{x:02d}.{y:02d}",
            Nazwa=f"Gatunek 01.{x:02d}.{y:02d}",
            Uprawy=lista_upraw,
        ))
    lista_kategorii.append(Kategoria(
        IdKategoria=f"01.{x:02d}",
        Nazwa=f"Kategoria 01.{x:02d}",
        Gatunki=lista_gatunek,
    ))


@get("/")
async def index() -> Template:
    return Template(template_name="slownik.jinja", context={"kategorie": lista_kategorii}, media_type=HTML_MEDIA)


@get("/jak-to-dziala")
async def jak_to_dziala() -> Template:
    return Template(template_name="jak_to_dziala.jinja", media_type=HTML_MEDIA)


@get("/api")
async def slownik() -> Template:
    return Template(template_name="api.jinja", media_type=HTML_MEDIA)



template_config = TemplateConfig(
    directory=Path(__file__).resolve().parent.parent / "templates",
    engine=JinjaTemplateEngine,
)

route_handlers: Sequence[ControllerRouterHandler] = [
    index, jak_to_dziala, slownik,
    create_static_files_router(directories=[Path(__file__).resolve().parent.parent / "static"], path="/static")
]

app = Litestar(
    route_handlers=route_handlers,
    template_config=template_config,
    debug=True,
    plugins=[],
    dependencies={"conn": connection},
    on_startup=[run_fixture],
    on_shutdown=[close_connection],
)

