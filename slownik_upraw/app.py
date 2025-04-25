import io
import sqlite3 as s3
from dataclasses import dataclass, field
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
from litestar.response import Template

from slownik_upraw.db import connection, close_connection, build_schema, load_data


HTML_MEDIA: str = MediaType.HTML


@dataclass
class Node:
    nazwa: str
    values: list = field(default_factory=list)


uprawa_headers = [
    "Id Uprawy",
    "Id Podkategorii",
    "Nazwa Uprawy",
    "Nazwa Łacińska Uprawy",
    "Synonimy Nazwy Uprawy",
    "Opis Uprawy",
    "Uwagi do Uprawy",
    "Produkt Rolny",
    "Uprawa Miododajna",
    "Uprawa Ekologiczna",
    "Uprawa Energetyczna",
    "Uprawa Ogrodnicza",
    "Dostawy Bezpośrednie",
    "Rolniczy Handel Detaliczny",
    "Dział Specjalny Produkcji Rolnej",
    "Okrywa Zimowa",
    "Warzywo",
    "Warzywo / Owoc / Kwiat / Zioło"
]



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


@get("/test")
async def test() -> Template:
    return Template(
        template_name="test.jinja",
        media_type=HTML_MEDIA,
    )


@get("/")
async def index(conn: s3.Connection) -> Template:
    form = UprawaForm()
    grupa: dict[str, Node] = {}
    klasa: dict[str, Node] = {}
    kategoria: dict[str, Node] = {}
    podkategoria: dict[str, Node] = {}

    res = conn.execute("""
    SELECT
    g.IdGrupa,
    g.NazwaGrupa,
    kla.IdKlasa,
    kla.NazwaKlasa,
    k.IdKategoria,
    k.NazwaKategoria,
    pk.IdPodKategoria,
    pk.NazwaPodKategoria,
    u.*
    FROM
        "Uprawa" AS u
    JOIN
        "PodKategoria" AS pk ON u."IdPodKategoria" = pk."IdPodKategoria"
    JOIN
        "Kategoria" AS k ON pk."IdKategoria" = k."IdKategoria"
    JOIN
        "Klasa" AS kla ON k."IdKlasa" = kla."IdKlasa"
    JOIN
        "Grupa" AS g ON kla."IdGrupa" = g."IdGrupa"              

    """).fetchall()

    for line in res:
        if line[0] not in grupa:
            grupa[line[0]] = Node(nazwa=line[1])    
        if line[2] not in klasa:
            klasa[line[2]] = Node(nazwa=line[3])
            grupa[line[0]].values.append(klasa[line[2]])
        if line[4] not in kategoria:
            kategoria[line[4]] = Node(nazwa=line[5])
            klasa[line[2]].values.append(kategoria[line[4]])
        if line[6] not in podkategoria:
            podkategoria[line[6]] = Node(nazwa=line[7])
            kategoria[line[4]].values.append(podkategoria[line[6]])
        podkategoria[line[6]].values.append(line[8:])
    
    # return str(list(grupa.values())[0].values[0].values[0].values[0].values[0])

    return Template(
        template_name="slownik.jinja", 
        context={
            "headers": uprawa_headers,
            "grupy": grupa.values(),
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
    test,
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

