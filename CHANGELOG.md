# Journal des versions

## Non publié

## v0.3.1
Correctifs, constatés en habillant meteo-planeur (interface Alpine.js).
- Les éléments `<template>` (gabarits d'Alpine, de Vue…) restent masqués et ne comptent plus comme premier ou dernier élément d'un composant. Avant, `.ui-range__ticks > *` en faisait une graduation invisible de plus, qui décalait toutes les graduations par rapport au curseur ; même défaut pour les légendes (`ui-legend__ticks`) et la bordure du dernier bouton de `ui-segmented`.
- La longueur de ligne des paragraphes (`--ui-measure`, 70 caractères) ne s'applique plus qu'au contenu des pages (`.ui-main p`) : dans une interface d'application, un paragraphe occupe la largeur de son bloc.

## v0.3.0
Composants d'application, pour les interfaces riches comme meteo-planeur (carte, graphiques, réglages). L'état passe par les attributs d'accessibilité (`aria-selected`, `aria-pressed`, `aria-expanded`, `aria-current`) : ils marchent avec n'importe quel JavaScript (Alpine…) comme avec des pages sans script. Aucune classe existante n'est renommée.
- La couleur de l'élément actif (`--ui-color-active`) passe du magenta au **cyan** (`#005761` en clair, `#5fd0dc` en sombre, 7:1 de contraste au moins) : sur les écrans de cockpit, le cyan marque les valeurs choisies par le pilote, et il se distingue nettement du bleu des boutons.
- `ui-tabs` (macro `tabs`) : onglets, choisi souligné en cyan.
- `ui-segmented` (macro `segmented`) : choix exclusif par boutons `aria-pressed` ou boutons radio ; variantes `--sm` et `--spaced` (boutons séparés sur deux lignes, pour les journées).
- `ui-menu` (macro `menu`) : menu déroulant, en `<details>` sans script ou piloté par `aria-expanded` ; éléments `ui-menu__item`, séparateur `ui-menu__sep`.
- `ui-range` (macro `slider`) : curseur cyan, graduations `ui-range__ticks` ; `ui-stepper` pour l'encadrer de boutons précédent / suivant.
- `ui-legend` (macro `legend`) : légende de carte, échelle en dégradé avec graduations ou catégories à pastilles.
- `ui-toolbar` : barre de réglages ; `ui-progress` (macro `progress`) : progression, déterminée ou non ; `ui-check` : cases à cocher ; `ui-select` : liste déroulante ; `ui-dialog` : fenêtre modale.
- Boutons `ui-btn--sm` et `ui-btn--icon`.
- Mise en page plein écran : `ui-body--app` (nouveau bloc `body_class` dans `ui/base.html`), `ui-split`, `ui-fill`, `ui-pane`, `ui-overlay--*` pour poser une légende sur une carte. Page de démonstration `/_charte/plein-ecran`.
- Nouveau bloc `header_end` et classe `ui-header__end` pour des commandes dans l'en-tête.
- Choix du thème : macro `theme_switch` et script `ui-kit.js` (chargé par `ui/base.html`, sans dépendance) qui applique le thème mémorisé avant l'affichage et ferme les menus par un clic à l'extérieur ou Échap. Clé `localStorage` « theme », la même que meteo-planeur.
- Nouvelle variable `--ui-shadow-overlay`, réservée aux éléments flottants (menus, fenêtres).

## v0.2.0
Nouvelle identité, sobre et dense, inspirée de l'aéronautique. Aucune classe ni variable existante n'est renommée ou supprimée.
- Couleurs : encre marine, fond gris froid, bleu pour les liens et les actions ; thème sombre « cockpit de nuit ».
- Magenta réservé à ce qui est actif (convention des écrans de cockpit) : page courante, ligne de tableau sélectionnée (`<tr aria-selected="true">`), focus clavier. Nouvelles variables `--ui-color-active` et `--ui-color-active-bg`.
- Police IBM Plex Sans intégrée (licence OFL, aucun appel externe) : zéro sans barre, I majuscule à empattements, chiffres à chasse fixe ; échelle typographique resserrée.
- Contrastes renforcés : texte et texte secondaire au niveau AAA (7:1 au moins) dans les deux thèmes, bordures des champs à 3:1 au moins.
- Panneaux plats (sans ombre), un seul rayon de 4 px ; en-tête de 3 rem, page courante soulignée, navigation qui défile sur petit écran.
- Nouveau composant `ui-data` et macro `data` : libellé, valeur, unité, en grille ou en liste.
- Nouvelle classe `ui-compact` : espacements et hauteur des contrôles réduits.
- Nouveaux instruments, avec les conventions du cockpit :
  - `ui-gauge` et macro `gauge` : jauge graduée à arcs colorés et index, lue comme un anémomètre (`role="meter"`) ;
  - `ui-wind` et macro `wind` : flèche de vent orientée selon la convention météo, « 250° / 15 kt », rafales en `G`.
- Nombres à la française dans les macros (virgule décimale, espace fine pour les milliers).
- État vide illustré par la silhouette de planeur.
- Choix du thème possible avec `<html data-theme="light|dark">` (sinon celui du système).
- Nouvelles variables : `--ui-color-surface-2`, `--ui-color-border-strong`, `--ui-text-xs`, `--ui-measure`, `--ui-control-height`, `--ui-header-height`.
- Pictogramme planeur dans l'en-tête et l'icône d'onglet.

## v0.1.0
- Première version : jetons de design (clair et sombre), mise en page, en-tête et navigation, boutons, cartes, messages, champs de formulaire, tableaux, pastilles, état vide.
- Page de démonstration `/_charte`.
