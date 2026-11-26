from pathlib import Path

import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route
from starlette.testclient import TestClient

import ui_kit
from ui_kit import NavItem, setup


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    (tmp_path / "page.html").write_text(
        '{% extends "ui/base.html" %}'
        '{% import "ui/macros.html" as ui_c %}'
        "{% block content %}<h1>Bonjour</h1>{{ ui_c.button('OK') }}{% endblock %}",
        encoding="utf-8",
    )

    async def page(request: Request):
        return templates.TemplateResponse(request, "page.html")

    app = Starlette(routes=[Route("/", page), Route("/comptes", page)])
    templates = setup(
        app,
        tmp_path,
        app_name="Démo",
        nav=[NavItem("Accueil", "/"), NavItem("Comptes", "/comptes")],
    )
    return TestClient(app)


def test_page_extends_base_layout(client: TestClient) -> None:
    html = client.get("/").text
    assert "<h1>Bonjour</h1>" in html
    assert 'href="/_ui/ui-kit.css?v=' + ui_kit.__version__ in html
    assert "Démo" in html
    assert 'class="ui-btn ui-btn--primary"' in html


def test_current_page_is_marked_in_nav(client: TestClient) -> None:
    html = client.get("/comptes").text
    assert 'href="/comptes" aria-current="page"' in html
    assert 'href="/" aria-current="page"' not in html


def test_static_files_are_served(client: TestClient) -> None:
    response = client.get("/_ui/ui-kit.css")
    assert response.status_code == 200
    assert "--ui-color-accent" in response.text


def test_demo_page_renders_every_component(client: TestClient) -> None:
    html = client.get(ui_kit.DEMO_URL).text
    components = (
        "ui-btn",
        "ui-card",
        "ui-alert",
        "ui-field",
        "ui-table",
        "ui-badge",
        "ui-empty",
        "ui-data",
        "ui-compact",
    )
    for css_class in components:
        assert css_class in html


def test_data_macro_renders_label_value_and_unit(tmp_path: Path) -> None:
    (tmp_path / "donnees.html").write_text(
        '{% import "ui/macros.html" as ui_c %}'
        '{{ ui_c.data([("Plafond", "2 150", "m"), ("Début", "11 h 30")], layout="list") }}',
        encoding="utf-8",
    )
    app = Starlette()
    templates = setup(app, tmp_path, app_name="Démo", demo=False)
    html = templates.get_template("donnees.html").render()
    assert 'class="ui-data ui-data--list"' in html
    assert "<dt>Plafond</dt>" in html
    assert '<span class="ui-data__value">2 150</span><span class="ui-data__unit">m</span>' in html
    assert '<span class="ui-data__value">11 h 30</span></dd>' in html


def test_font_and_mark_are_served(client: TestClient) -> None:
    for path in ("fonts/atkinson-hyperlegible-next.woff2", "fonts/OFL.txt", "mark.svg"):
        assert client.get(f"/_ui/{path}").status_code == 200, path
    css = client.get("/_ui/ui-kit.css").text
    assert '[data-theme="dark"]' in css
    assert "--ui-color-active" in css
