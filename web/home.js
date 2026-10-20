/* Home page behaviour: build the volume list from the generated manifest. */
(() => {
  "use strict";

  const manifest = window.MUSOKU_MANIFEST || {};
  const root = document.documentElement;
  const grid = document.getElementById("volumeGrid");
  const stats = document.getElementById("mastheadStats");
  const themeToggle = document.getElementById("themeToggle");

  const SUN_ICON = `<svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <circle cx="12" cy="12" r="4"/>
    <path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M18.7 5.3l-1.4 1.4M6.7 17.3l-1.4 1.4"/>
  </svg>`;
  const MOON_ICON = `<svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M20 15.5A8.5 8.5 0 0 1 8.5 4 8.5 8.5 0 1 0 20 15.5Z"/>
  </svg>`;

  function readTheme() {
    try {
      return localStorage.getItem("mt15:theme") || "light";
    } catch {
      return "light";
    }
  }

  function writeTheme(theme) {
    try {
      localStorage.setItem("mt15:theme", theme);
    } catch {
      /* Private browsing: the page still works, the choice is just not kept. */
    }
  }

  function applyTheme(theme) {
    root.dataset.theme = theme;
    if (!themeToggle) return;
    const dark = theme === "dark";
    themeToggle.innerHTML = dark ? SUN_ICON : MOON_ICON;
    themeToggle.setAttribute(
      "aria-label",
      dark ? "Switch to light theme" : "Switch to dark theme"
    );
    themeToggle.setAttribute(
      "title",
      dark ? "Switch to light theme" : "Switch to dark theme"
    );
  }

  function formatNumber(value) {
    return new Intl.NumberFormat("en-US").format(Number(value) || 0);
  }

  function volumeTitle(entry) {
    return entry.label || entry.title || `Volume ${entry.number}`;
  }

  function render() {
    const numbers = Object.keys(manifest)
      .map((key) => Number(key))
      .filter((number) => Number.isFinite(number))
      .sort((a, b) => a - b);

    if (!numbers.length) {
      grid.innerHTML =
        '<p class="section-note">The volume list is unavailable. Run <code>python3 scripts/export_web.py</code> to rebuild it.</p>';
      return;
    }

    let chapters = 0;
    let scenes = 0;
    let words = 0;
    let lines = 0;

    grid.innerHTML = numbers
      .map((number) => {
        const entry = manifest[String(number)];
        chapters += entry.chapters || 0;
        scenes += entry.scenes || 0;
        words += entry.words || 0;
        lines += entry.speechBlocks || 0;

        return `
          <article class="volume-card">
            <img class="volume-card__cover" src="images/${entry.slug}/CoverDesign.jpg"
                 width="1403" height="2000" loading="lazy" decoding="async"
                 alt="Cover of Mushoku Tensei Volume ${number}">
            <div class="volume-card__body">
              <p class="volume-card__kicker">
                <span>Mushoku Tensei</span>
                <span class="volume-card__number">${number}</span>
              </p>
              <h3>${volumeTitle(entry)}</h3>
              <p>${entry.blurb || ""}</p>
              <p class="volume-card__meta">
                <span>${formatNumber(entry.chapters)} chapters</span>
                <span>${formatNumber(entry.scenes)} scenes</span>
                <span>${formatNumber(entry.words)} words</span>
                <span>${formatNumber(entry.speechBlocks)} lines</span>
              </p>
              <a class="volume-card__link" href="reader.html?volume=${number}">Read volume ${number}</a>
            </div>
          </article>`;
      })
      .join("");

    stats.innerHTML = `
      <span><strong>${numbers.length}</strong>volumes</span>
      <span><strong>${formatNumber(chapters)}</strong>chapters</span>
      <span><strong>${formatNumber(scenes)}</strong>scenes</span>
      <span><strong>${formatNumber(lines)}</strong>spoken lines</span>
      <span><strong>${formatNumber(words)}</strong>words</span>`;
  }

  applyTheme(readTheme());

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const next = root.dataset.theme === "dark" ? "light" : "dark";
      applyTheme(next);
      writeTheme(next);
    });
  }

  render();
})();
