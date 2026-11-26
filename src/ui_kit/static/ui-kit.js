// ui-kit : petits comportements, sans dépendance. Chargé dans le <head>.
// - Thème (auto, clair, sombre) : appliqué avant l'affichage pour éviter un éclair de
//   l'autre thème, puis boutons [data-ui-theme] (macro theme_switch). Choix gardé dans
//   localStorage sous la clé « theme ».
// - Menus <details class="ui-menu"> : fermés par un clic à l'extérieur ou la touche Échap.
(function () {
  var racine = document.documentElement;

  function lireTheme() {
    try {
      var t = localStorage.getItem("theme");
      return t === "light" || t === "dark" ? t : "auto";
    } catch (e) {
      return "auto";
    }
  }

  function appliquerTheme(theme) {
    if (theme === "light" || theme === "dark") racine.dataset.theme = theme;
    else delete racine.dataset.theme;
    document.querySelectorAll("[data-ui-theme]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.uiTheme === theme));
    });
  }

  function choisirTheme(theme) {
    try {
      if (theme === "auto") localStorage.removeItem("theme");
      else localStorage.setItem("theme", theme);
    } catch (e) {}
    appliquerTheme(theme);
  }

  function fermerMenus(sauf) {
    document.querySelectorAll("details.ui-menu[open]").forEach(function (m) {
      if (m !== sauf) m.removeAttribute("open");
    });
  }

  appliquerTheme(lireTheme());

  document.addEventListener("DOMContentLoaded", function () {
    appliquerTheme(lireTheme());
  });

  document.addEventListener("click", function (ev) {
    var bouton = ev.target.closest("[data-ui-theme]");
    if (bouton) choisirTheme(bouton.dataset.uiTheme);
    fermerMenus(ev.target.closest("details.ui-menu"));
  });

  document.addEventListener("keydown", function (ev) {
    if (ev.key !== "Escape") return;
    var ouvert = document.querySelector("details.ui-menu[open]");
    if (!ouvert) return;
    fermerMenus(null);
    var resume = ouvert.querySelector("summary");
    if (resume) resume.focus();
  });
})();
