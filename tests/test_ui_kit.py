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
    components = ("ui-btn", "ui-card", "ui-alert", "ui-field", "ui-table", "ui-badge", "ui-empty")
    for css_class in components:
        assert css_class in html
