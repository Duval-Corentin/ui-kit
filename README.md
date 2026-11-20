# ui-kit

Charte graphique commune à toutes les applis de la plateforme : variables CSS, composants, gabarit de page Jinja.

## Installation dans une appli

Dans le `pyproject.toml` de l'appli (c'est déjà fait par `app-template`) :

```toml
dependencies = ["ui-kit @ git+https://github.com/Duval-Corentin/ui-kit@v0.1.0"]
```

Le dépôt est **privé**. Chaque appli l'installe avec le secret `UI_KIT_TOKEN` (jeton GitHub en lecture seule sur ce seul dépôt), dans sa CI, à la construction de son image Docker et pour Dependabot. En local, `gh auth setup-git` suffit.

## Utilisation

```python
from ui_kit import NavItem, setup

templates = setup(
    app,
    templates_dir,
    app_name="Budget",
    nav=[NavItem("Accueil", "/"), NavItem("Comptes", "/comptes")],
)
```

```html+jinja
{% extends "ui/base.html" %}
{% import "ui/macros.html" as ui_c %}
{% block content %}
  <h1>Mes comptes</h1>
  {% call ui_c.card("Solde") %}1 250 €{% endcall %}
  {{ ui_c.button("Ajouter", href="/comptes/nouveau") }}
{% endblock %}
```

La page **`/_charte`** de chaque appli montre tous les composants. Elle sert à vérifier le rendu après une mise à jour.

## Contenu

- `static/ui-kit.css` : jetons de design (couleurs, typographie, espacements, avec thème sombre automatique) et composants `ui-*`.
- `templates/ui/base.html` : structure de page (en-tête, navigation, contenu, pied de page). Blocs : `title`, `head`, `nav`, `flash`, `content`, `footer`, `scripts`.
- `templates/ui/macros.html` : `button`, `card`, `alert`, `field`, `badge`, `empty`.

## Publier une nouvelle version

1. Modifier, mettre à jour `CHANGELOG.md`, puis augmenter la version dans `pyproject.toml` **et** `src/ui_kit/__init__.py`.
2. Merger, puis créer le tag : `git tag v0.2.0 && git push --tags`.
3. Dans chaque appli, une PR change `@v0.1.0` en `@v0.2.0`, lance `uv lock`, et vérifie `/_charte`.

Versionnement : **correctif** (0.1.x) pour un ajustement visuel, **mineure** (0.x.0) pour un nouveau composant, **majeure** pour un changement qui casse les gabarits existants (classe renommée, bloc supprimé).
