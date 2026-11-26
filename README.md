# ui-kit

Charte graphique commune à toutes les applis de la plateforme : variables CSS, composants, gabarit de page Jinja.

## Installation dans une appli

Dans le `pyproject.toml` de l'appli (c'est déjà fait par `app-template`) :

```toml
dependencies = ["ui-kit @ git+https://github.com/Duval-Corentin/ui-kit@v0.3.0"]
```

Le dépôt doit être **public** pour que l'installation fonctionne sans jeton, dans la CI comme dans Docker. Il ne contient que du CSS et des gabarits.

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
- `templates/ui/base.html` : structure de page (en-tête, navigation, contenu, pied de page). Blocs : `title`, `head`, `body_class`, `nav`, `header_end`, `flash`, `content`, `footer`, `scripts`.
- `templates/ui/macros.html` : `button`, `card`, `alert`, `field`, `badge`, `data`, `gauge`, `wind`, `empty`, et pour les applications riches `tabs`, `segmented`, `menu`, `slider`, `legend`, `progress`, `theme_switch`.
- `static/ui-kit.js` : choix du thème et fermeture des menus, sans dépendance (chargé par `ui/base.html`).
- `static/fonts/` : police IBM Plex Sans (licence OFL).

## Repères de la charte

- Sobre et dense : panneaux plats, un seul rayon, une échelle de texte resserrée.
- Le **cyan** (`--ui-color-active`) signale uniquement ce qui est actif : page courante, ligne sélectionnée (`<tr aria-selected="true">`), focus. Ne pas l'utiliser pour décorer.
- Valeurs chiffrées : `ui_c.data([("Plafond", "2 150", "m")])`, ou la classe `num` dans les tableaux.
- Instruments : `ui_c.gauge("Vent au sol", 18, "kt", max=40, step=5, zones=[(0, 15, "success"), (15, 25, "warning"), (25, 40, "danger")])` et `ui_c.wind(250, 15, gust=25)`.
- Écrans riches : ajouter `ui-compact` sur un conteneur.
- Thème : celui du système par défaut ; `<html data-theme="dark">` ou `"light"` pour l'imposer. La macro `theme_switch()` affiche le choix Auto / Clair / Sombre.
- Application plein écran (carte, tableau de bord) : `{% block body_class %} ui-body--app{% endblock %}`, puis `ui-toolbar`, `ui-split` (`ui-fill` + `ui-pane`) et `ui-overlay--bottom-left` pour une légende sur la carte. Exemple complet sur `/_charte/plein-ecran`.
- Composants pilotés en JavaScript : l'état se donne par les attributs ARIA (`aria-selected` pour un onglet, `aria-pressed` pour un choix, `aria-expanded` pour un menu, `aria-current` pour une graduation), jamais par une classe.

## Publier une nouvelle version

1. Modifier, mettre à jour `CHANGELOG.md`, puis augmenter la version dans `pyproject.toml` **et** `src/ui_kit/__init__.py`.
2. Merger, puis créer le tag : `git tag v0.2.0 && git push --tags`.
3. Dans chaque appli, une PR change `@v0.1.0` en `@v0.2.0`, lance `uv lock`, et vérifie `/_charte`.

Versionnement : **correctif** (0.1.x) pour un ajustement visuel, **mineure** (0.x.0) pour un nouveau composant, **majeure** pour un changement qui casse les gabarits existants (classe renommée, bloc supprimé).
