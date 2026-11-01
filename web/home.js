/* Home page behaviour: build the volume list from the generated manifest. */
(() => {
  "use strict";

  const manifest = window.MUSOKU_MANIFEST || {};
  const root = document.documentElement;
  const grid = document.getElementById("volumeGrid");
  const feature = document.getElementById("featuredVolume");
  const libraryLine = document.getElementById("libraryLine");
  const continueReading = document.getElementById("continueReading");
  const themeToggle = document.getElementById("themeToggle");

  const SUN_ICON = `<svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <circle cx="12" cy="12" r="4"/>
    <path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M18.7 5.3l-1.4 1.4M6.7 17.3l-1.4 1.4"/>
  </svg>`;
  const MOON_ICON = `<svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M20 15.5A8.5 8.5 0 0 1 8.5 4 8.5 8.5 0 1 0 20 15.5Z"/>
  </svg>`;
  const ARROW_ICON = `<svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>`;

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (character) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    }[character]));
  }

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
    return entry.label || entry.title || "Untitled volume";
  }

  function readStored(key, fallback) {
    try {
      const value = localStorage.getItem(key);
      return value === null ? fallback : value;
    } catch {
      return fallback;
    }
  }

  function resumeFor(number) {
    return readStored(`mt15:v${number}:chapter-label`, "");
  }

  function renderFeature(number, isLast) {
    const entry = manifest[String(number)];
    if (!entry) return "";
    const chapter = resumeFor(number);
    const title = volumeTitle(entry);
    const href = `reader.html?volume=${number}`;
    const action = isLast ? "Continue" : "Open";
    const actionLabel = chapter
      ? `${action} Volume ${number}, ${chapter}`
      : `${action} Volume ${number}`;

    return `
      <figure class="feature">
        <a class="feature__plate" href="${href}" aria-label="${escapeHtml(actionLabel)}">
          <img src="images/${escapeHtml(entry.slug)}/CoverDesign.jpg"
               width="900" height="1283" decoding="async" fetchpriority="high"
               alt="">
        </a>
        <figcaption class="feature__caption">
          <p class="feature__kicker">${isLast ? "Last read" : "First in the edition"}</p>
          <p class="feature__title">Volume ${number}</p>
          <p class="feature__subtitle">${escapeHtml(title)}</p>
          <p class="feature__chapter">${chapter
            ? escapeHtml(chapter)
            : `${formatNumber(entry.chapters)} chapters`}</p>
        </figcaption>
      </figure>`;
  }

  function renderShelfRow(number, isLast) {
    const entry = manifest[String(number)];
    const chapter = resumeFor(number);
    const title = volumeTitle(entry);
    const blurb = entry.blurb || "";
    const facts = [
      ["Chapters", formatNumber(entry.chapters)],
      ["Scenes", formatNumber(entry.scenes)],
      ["Words", formatNumber(entry.words)],
      ["Lines", formatNumber(entry.speechBlocks)],
    ];
    const spoken = isLast
      ? chapter
        ? ` Last read: ${chapter}.`
        : " Last read."
      : "";
    const label = `Volume ${number}, ${title}. ${formatNumber(entry.chapters)} chapters, ${formatNumber(entry.scenes)} scenes, ${formatNumber(entry.words)} words, ${formatNumber(entry.speechBlocks)} attributed lines.${spoken}`;

    return `
      <li>
        <a class="shelf-row" href="reader.html?volume=${number}" aria-label="${escapeHtml(label)}">
          <span class="shelf-row__cover">
            <img src="images/${escapeHtml(entry.slug)}/thumb.jpg"
                 width="180" height="257" loading="lazy" decoding="async" alt="">
          </span>
          <div class="shelf-row__title">
            <span class="shelf-row__volume">Volume ${number}</span>
            <h3 class="shelf-row__name">${escapeHtml(title)}</h3>
            ${blurb ? `<span class="shelf-row__blurb">${escapeHtml(blurb)}</span>` : ""}
          </div>
          <span class="shelf-row__facts">
            ${facts
              .map(
                ([factLabel, value]) => `
              <span class="shelf-row__fact">
                <span class="shelf-row__label">${factLabel}</span>
                <span class="shelf-row__value">${value}</span>
              </span>`
              )
              .join("")}
          </span>
          <span class="shelf-row__state">
            ${isLast ? '<span class="tag tag--reading">Reading</span>' : ""}
            ${isLast && chapter ? `<span class="shelf-row__chapter">${escapeHtml(chapter)}</span>` : ""}
          </span>
          <span class="shelf-row__go" aria-hidden="true">${ARROW_ICON}</span>
        </a>
      </li>`;
  }

  function setContinue(hasLast, last) {
    if (!continueReading) return;
    if (!hasLast) {
      continueReading.hidden = true;
      return;
    }
    const chapter = resumeFor(last);
    continueReading.href = `reader.html?volume=${last}`;
    continueReading.textContent = `Continue Volume ${last}`;
    continueReading.setAttribute(
      "aria-label",
      chapter ? `Continue Volume ${last}, ${chapter}` : `Continue Volume ${last}`
    );
    continueReading.hidden = false;
  }

  function render() {
    const numbers = Object.keys(manifest)
      .map((key) => Number(key))
      .filter((number) => Number.isFinite(number))
      .sort((a, b) => a - b);

    if (!numbers.length) {
      if (grid) {
        grid.innerHTML =
          '<li><p class="load-error">The volume list is unavailable. Run <code>python3 scripts/export_web.py</code> to rebuild it.</p></li>';
      }
      if (feature) feature.innerHTML = "";
      if (continueReading) continueReading.hidden = true;
      return;
    }

    const last = Number(readStored("mt15:last-volume", "0"));
    const hasLast = Boolean(manifest[String(last)]);
    const featuredNumber = hasLast ? last : numbers[0];

    let chapters = 0;
    let words = 0;

    if (grid) {
      grid.innerHTML = numbers
        .map((number) => {
          const entry = manifest[String(number)];
          chapters += entry.chapters || 0;
          words += entry.words || 0;
          return renderShelfRow(number, number === last && hasLast);
        })
        .join("");
    }

    if (feature) feature.innerHTML = renderFeature(featuredNumber, hasLast);

    if (libraryLine) {
      libraryLine.textContent =
        `${numbers.length} volumes, ${formatNumber(chapters)} chapters, ${formatNumber(words)} words`;
    }

    setContinue(hasLast, last);
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
