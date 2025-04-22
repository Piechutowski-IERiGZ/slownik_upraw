import io
import sqlite3 as s3
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
from csv import writer

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from wtforms import Form, BooleanField, StringField

from litestar import Litestar, MediaType, Response, get
from litestar.types import ControllerRouterHandler
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import create_static_files_router
from litestar.template import TemplateConfig
from litestar.response import Template, File

from slownik_upraw.db import connection, close_connection, build_schema, load_data


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



class UprawaForm(Form):
    IdUprawa = StringField("Id Uprawy")
    IdPodKategoria = StringField("Id Pod Kategorii")

    NazwaUprawa = StringField("Nazwa Uprawy")
    NazwaLacinskaUprawa = StringField("Nazwa Łacińska Uprawy")
    NazwaSynonimyUprawa = StringField("Synonimy Nazwy Uprawy")
    OpisUprawa = StringField("Opis Uprawy")
    UwagaUprawa = StringField("Uwagi do Uprawy")
    
    ProduktRolny = BooleanField("Produkt Rolny")
    UprawaMiododajna = BooleanField("Uprawa Miododajna")
    UprawaEkologiczna = BooleanField("Uprawa Ekologiczna")
    UprawaEnergetyczna = BooleanField("Uprawa Energetyczna")
    UprawaOgrodnicza = BooleanField("Uprawa Ogrodnicza")
    DostawyBezposrednie = BooleanField("Dostawy Bezpośrednie")
    RolniczyHandelDetaliczny = BooleanField("Rolniczy Handel Detaliczny")
    DzialSpecjalny = BooleanField("Dział Specjalny Produkcji Rolnej")
    OkrywaZimowa = BooleanField("Okrywa Zimowa")
    Warzywo = BooleanField("Warzywo")
    WarzywoOwocKwiatZiolo = BooleanField("Warzywo/Owoc/Kwiat/Zioło")




@get("/")
async def index() -> Template:
    form = UprawaForm()
    return Template(
        template_name="slownik.jinja", 
        context={
            "kategorie": lista_kategorii,
            "form": form,
        }, 
        media_type=HTML_MEDIA,
    )


@get("/download-form")
async def download_form() -> Response[bytes]:
    data = [
        ["Name", "Age", "City"],
        ["Alice", 30, "New York"],
        ["Bob", 25, "London"],
        ["Charlie", 35, "Paris"]
    ]

    output = io.StringIO()
    new_file = writer(output)
    new_file.writerows(data)
    output.seek(0)
    bytes_buffer = io.BytesIO(output.getvalue().encode("utf-8"))
    return bytes_buffer




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
    index, 
    jak_to_dziala, 
    slownik, 
    download_form,  
    create_static_files_router(directories=[Path(__file__).resolve().parent.parent / "static"], path="/static"),
]

app = Litestar(
    route_handlers=route_handlers,
    template_config=template_config,
    debug=True,
    plugins=[],
    dependencies={"conn": connection},
    on_startup=[build_schema, load_data],
    on_shutdown=[close_connection],
)

