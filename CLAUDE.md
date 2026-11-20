# ui-kit : contexte pour Claude

Charte graphique partagée par toutes les applis. Lis `README.md`.

## Principes
- Tout ce qui est visuel passe par des variables CSS `--ui-*` et des classes `ui-*`. Pas de couleur ni de taille en dur dans les composants.
- Chaque composant fonctionne en thème clair et sombre, se contrôle au clavier (focus visible) et garde un contraste suffisant (WCAG AA).
- Un nouveau composant = une classe CSS + une macro dans `macros.html` (si utile) + un exemple dans `demo.html` + un test.
- Ne renomme ni ne supprime une classe ou un bloc existant sans version majeure : toutes les applis en dépendent.

## Avant de finir une tâche
- `uv run ruff check . && uv run ruff format --check . && uv run pytest`
- Mets à jour `CHANGELOG.md` (section « Non publié »).
- Dans la PR, indique le type de version à publier (correctif, mineure ou majeure).
