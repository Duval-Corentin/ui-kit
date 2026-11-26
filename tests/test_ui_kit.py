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
        "ui-gauge",
        "ui-wind",
        "ui-tabs",
        "ui-segmented",
        "ui-menu",
        "ui-range",
        "ui-legend",
        "ui-progress",
        "ui-check",
        "ui-select",
        "ui-dialog",
        "data-ui-theme",
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
    for path in ("fonts/ibm-plex-sans.woff2", "fonts/OFL.txt", "mark.svg"):
        assert client.get(f"/_ui/{path}").status_code == 200, path
    css = client.get("/_ui/ui-kit.css").text
    assert '[data-theme="dark"]' in css
    assert "--ui-color-active" in css


def test_gauge_and_wind_macros(tmp_path: Path) -> None:
    (tmp_path / "instruments.html").write_text(
        '{% import "ui/macros.html" as ui_c %}'
        '{{ ui_c.gauge("Vent", 18, "kt", max=40, step=5, zones=[(15, 25, "warning")]) }}'
        "{{ ui_c.wind(50, 12, gust=20) }}",
        encoding="utf-8",
    )
    templates = setup(Starlette(), tmp_path, app_name="Démo", demo=False)
    html = templates.get_template("instruments.html").render()
    assert 'role="meter"' in html and 'aria-valuenow="18"' in html
    assert "--ui-gauge-pos: 45.00%" in html
    assert html.count('class="ui-gauge__tick"') == 9
    assert 'ui-gauge__arc--warning" style="--from: 37.50%; --to: 62.50%"' in html
    assert html.count('class="ui-gauge__ticks"') == 1 and ">40</span>" in html
    assert "--ui-wind-dir: 50deg" in html
    assert "050° / 12G20 kt" in html
    assert 'aria-label="Vent du 50°, 12 kt, rafales 20 kt"' in html


def test_numbers_are_written_the_french_way(tmp_path: Path) -> None:
    (tmp_path / "n.html").write_text(
        '{% import "ui/macros.html" as ui_c %}'
        '{{ ui_c.gauge("Plafond", 2150, max=3500, step=500) }}',
        encoding="utf-8",
    )
    html = setup(Starlette(), tmp_path, app_name="Démo", demo=False).get_template("n.html").render()
    assert "2\u202f150</span>" in html
    assert ">3\u202f500</span>" in html


def test_full_screen_demo_uses_app_layout(client: TestClient) -> None:
    html = client.get(ui_kit.DEMO_URL + "/plein-ecran").text
    assert 'class="ui-body ui-body--app"' in html
    for css_class in (
        "ui-toolbar",
        "ui-split",
        "ui-fill",
        "ui-pane",
        "ui-overlay",
        "ui-header__end",
    ):
        assert css_class in html
    assert client.get("/_ui/ui-kit.js").status_code == 200
    assert "/_ui/ui-kit.js?v=" in html


def test_application_macros(tmp_path: Path) -> None:
    (tmp_path / "app.html").write_text(
        '{% import "ui/macros.html" as ui_c %}'
        '{{ ui_c.tabs([("Carte", "/carte"), ("Manuel", "/manuel")], current="/manuel") }}'
        '{{ ui_c.segmented("modele", [("arome", "AROME"), ("arpege", "ARPEGE")], "arpege") }}'
        '{{ ui_c.slider("heure", "Heure", max=2, value=1, ticks=["10", "11", "12"]) }}'
        '{{ ui_c.legend("Niveau", items=[("Faible", "#f3c27a")]) }}'
        '{{ ui_c.progress("Préparation") }}',
        encoding="utf-8",
    )
    html = (
        setup(Starlette(), tmp_path, app_name="Démo", demo=False).get_template("app.html").render()
    )
    assert '<a href="/manuel" aria-current="page">Manuel</a>' in html
    assert '<a href="/carte">Carte</a>' in html
    assert 'value="arpege" checked>ARPEGE' in html
    assert 'value="arome">AROME' in html
    assert '<span aria-current="true">11</span>' in html
    assert 'style="--swatch: #f3c27a"' in html
    assert '<progress class="ui-progress" aria-label="Préparation" max="100"></progress>' in html


def test_templates_ignored_by_components(client: TestClient) -> None:
    """Les <template> d'Alpine ne comptent ni comme graduation, ni comme premier ou dernier."""
    css = client.get("/_ui/ui-kit.css").text
    assert "template { display: none !important; }" in css
    assert ".ui-range__ticks > :not(template)" in css and ".ui-range__ticks > *" not in css
    assert ".ui-legend__ticks > :nth-last-child(1 of :not(template))" in css
    assert ".ui-main p { max-width: var(--ui-measure); }" in css
