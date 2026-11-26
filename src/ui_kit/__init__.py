"""Charte graphique commune de la plateforme.

Utilisation dans une appli FastAPI (ou Starlette) :

    from ui_kit import NavItem, setup

    templates = setup(
        app,
        templates_dir=Path(__file__).parent / "templates",
        app_name="Budget",
        nav=[NavItem("Accueil", "/"), NavItem("Comptes", "/comptes")],
    )

Les gabarits de l'appli étendent ensuite ``ui/base.html`` et importent les
composants de ``ui/macros.html``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, select_autoescape
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

__version__ = "0.2.0"

PACKAGE_DIR = Path(__file__).resolve().parent
STATIC_DIR = PACKAGE_DIR / "static"
TEMPLATES_DIR = PACKAGE_DIR / "templates"
STATIC_URL = "/_ui"
DEMO_URL = "/_charte"

__all__ = ["DEMO_URL", "STATIC_URL", "NavItem", "__version__", "setup"]


@dataclass(frozen=True)
class NavItem:
    """Lien de la barre de navigation principale."""

    label: str
    href: str


def setup(
    app: Starlette,
    templates_dir: str | Path,
    *,
    app_name: str,
    nav: list[NavItem] | None = None,
    demo: bool = True,
) -> Jinja2Templates:
    """Branche la charte sur l'appli et renvoie le moteur de gabarits.

    - sert les fichiers statiques de la charte sous ``/_ui`` ;
    - cherche les gabarits d'abord dans ``templates_dir`` (l'appli), puis dans la charte ;
    - expose la variable ``ui`` à tous les gabarits (nom de l'appli, navigation, version) ;
    - si ``demo``, ajoute la page ``/_charte`` qui montre tous les composants.
    """
    app.mount(STATIC_URL, StaticFiles(directory=STATIC_DIR), name="ui_static")

    env = Environment(
        loader=ChoiceLoader(
            [
                FileSystemLoader(str(templates_dir)),
                FileSystemLoader(str(TEMPLATES_DIR)),
            ]
        ),
        autoescape=select_autoescape(["html", "xml"]),
    )
    env.globals["ui"] = {
        "app_name": app_name,
        "nav": list(nav or []),
        "static": STATIC_URL,
        "version": __version__,
    }
    templates = Jinja2Templates(env=env)

    if demo:

        async def charte(request: Request):
            return templates.TemplateResponse(request, "ui/demo.html")

        app.add_route(DEMO_URL, charte, include_in_schema=False)

    return templates
