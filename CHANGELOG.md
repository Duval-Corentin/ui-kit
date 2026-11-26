# Journal des versions

## Non publié

## v0.2.0
Nouvelle identité, sobre et dense, inspirée de l'aéronautique. Aucune classe ni variable existante n'est renommée ou supprimée.
- Couleurs : encre marine, fond gris froid, bleu pour les liens et les actions ; thème sombre « cockpit de nuit ».
- Magenta réservé à ce qui est actif (convention des écrans de cockpit) : page courante, ligne de tableau sélectionnée (`<tr aria-selected="true">`), focus clavier. Nouvelles variables `--ui-color-active` et `--ui-color-active-bg`.
- Police IBM Plex Sans intégrée (licence OFL, aucun appel externe) : zéro sans barre, I majuscule à empattements, chiffres à chasse fixe ; échelle typographique resserrée.
- Contrastes renforcés : texte et texte secondaire au niveau AAA (7:1 au moins) dans les deux thèmes, bordures des champs à 3:1 au moins.
- Panneaux plats (sans ombre), un seul rayon de 4 px ; en-tête de 3 rem, page courante soulignée, navigation qui défile sur petit écran.
- Nouveau composant `ui-data` et macro `data` : libellé, valeur, unité, en grille ou en liste.
- Nouvelle classe `ui-compact` : espacements et hauteur des contrôles réduits.
- Choix du thème possible avec `<html data-theme="light|dark">` (sinon celui du système).
- Nouvelles variables : `--ui-color-surface-2`, `--ui-color-border-strong`, `--ui-text-xs`, `--ui-measure`, `--ui-control-height`, `--ui-header-height`.
- Pictogramme planeur dans l'en-tête et l'icône d'onglet.

## v0.1.0
- Première version : jetons de design (clair et sombre), mise en page, en-tête et navigation, boutons, cartes, messages, champs de formulaire, tableaux, pastilles, état vide.
- Page de démonstration `/_charte`.
