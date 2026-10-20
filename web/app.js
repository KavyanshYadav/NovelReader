/* global window, document, localStorage, IntersectionObserver */
(() => {
  "use strict";

  const volumeManifest =
    window.MUSOKU_MANIFEST ||
    (window.VOLUME15_DATA
      ? {
          15: {
            number: 15,
            slug: "vol15",
            title: "Mushoku Tensei: Jobless Reincarnation Vol. 15",
            file: null,
          },
        }
      : null);
  const volumeOrder = volumeManifest
    ? Object.keys(volumeManifest)
        .map((number) => Number(number))
        .filter((number) => Number.isFinite(number))
        .sort((a, b) => a - b)
    : [];
  let data = null;
  let activeVolume = null;
  let switchingVolume = false;
  const reader = document.getElementById("reader");
  const chaptersRoot = document.getElementById("chapters");
  const toc = document.getElementById("toc");
  const currentChapter = document.getElementById("currentChapter");
  const progressBar = document.getElementById("progressBar");
  const themeToggle = document.getElementById("themeToggle");
  const fontDecrease = document.getElementById("fontDecrease");
  const fontIncrease = document.getElementById("fontIncrease");
  const menuToggle = document.getElementById("menuToggle");
  const sidebar = document.getElementById("sidebar");
  const sidebarOverlay = document.getElementById("sidebarOverlay");
  const backToTop = document.getElementById("backToTop");
  const toast = document.getElementById("toast");
  const root = document.documentElement;

  const appRoot = document.querySelector(".app");
  const openFocusButton = document.getElementById("openFocus");
  const openFocusHeroButton = document.getElementById("openFocusHero");
  const focusReader = document.getElementById("focusReader");
  const focusChapterKicker = document.getElementById("focusChapterKicker");
  const focusChapterTitle = document.getElementById("focusChapterTitle");
  const focusSceneMeta = document.getElementById("focusSceneMeta");
  const focusMain = document.getElementById("focusMain");
  const focusStatus = document.getElementById("focusStatus");
  const focusPrev = document.getElementById("focusPrev");
  const focusNext = document.getElementById("focusNext");
  const focusClose = document.getElementById("focusClose");
  const focusThemeToggle = document.getElementById("focusThemeToggle");
  const focusFontDecrease = document.getElementById("focusFontDecrease");
  const focusFontIncrease = document.getElementById("focusFontIncrease");
  const focusFullscreen = document.getElementById("focusFullscreen");
  const focusChromeToggle = document.getElementById("focusChromeToggle");
  const focusChromeReveal = document.getElementById("focusChromeReveal");
  const focusSettingsToggle = document.getElementById("focusSettingsToggle");
  const timeline = document.getElementById("timeline");
  const timelineScroller = document.getElementById("timelineScroller");
  const settingsToggle = document.getElementById("settingsToggle");
  const settingsPanel = document.getElementById("settingsPanel");
  const settingsScrim = document.getElementById("settingsScrim");
  const settingsClose = document.getElementById("settingsClose");
  const settingsFontDecrease = document.getElementById("settingsFontDecrease");
  const settingsFontIncrease = document.getElementById("settingsFontIncrease");
  const settingsFontValue = document.getElementById("settingsFontValue");
  const settingsReset = document.getElementById("settingsReset");
  const volumeButtons = document.getElementById("volumeButtons");
  const sidebarCover = document.getElementById("sidebarCover");
  const sidebarVolume = document.getElementById("sidebarVolume");
  const heroVolume = document.getElementById("heroVolume");
  const heroLede = document.getElementById("heroLede");
  const heroCover = document.getElementById("heroCover");
  const volumeEndTitle = document.getElementById("volumeEndTitle");
  const beginReading = document.getElementById("beginReading");
  const metaDescription = document.querySelector('meta[name="description"]');

  if (!volumeManifest || !volumeOrder.length) {
    reader.innerHTML = '<p class="load-error">The volume data could not be loaded. Make sure <code>data.js</code> is next to <code>index.html</code>.</p>';
    return;
  }

  const numberFormatter = new Intl.NumberFormat("en-US");
  const FONT_MIN = 17;
  const FONT_MAX = 24;
  const FONT_DEFAULT = 19;
  const TYPEFACE_VALUES = ["serif", "sans", "mono"];
  const LINE_HEIGHT_VALUES = {
    compact: "1.58",
    cozy: "1.78",
    airy: "2.02",
  };
  const READING_WIDTH_VALUES = {
    narrow: "660px",
    standard: "760px",
    wide: "900px",
  };
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const SUN_ICON = `<svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <circle cx="12" cy="12" r="4"/>
    <path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M18.7 5.3l-1.4 1.4M6.7 17.3l-1.4 1.4"/>
  </svg>`;
  const MOON_ICON = `<svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M20 15.5A8.5 8.5 0 0 1 8.5 4 8.5 8.5 0 1 0 20 15.5Z"/>
  </svg>`;

  const storage = {
    get(key) {
      try {
        return localStorage.getItem(key);
      } catch {
        return null;
      }
    },
    set(key, value) {
      try {
        localStorage.setItem(key, value);
      } catch {
        /* Private browsing or file:// restrictions: reading still works. */
      }
    },
  };

  function loadVolumeData(number) {
    return new Promise((resolve, reject) => {
      const store = (window.MUSOKU_VOLUME_DATA = window.MUSOKU_VOLUME_DATA || {});
      if (store[number]) {
        resolve(store[number]);
        return;
      }
      if (window.MUSOKU_VOLUMES && window.MUSOKU_VOLUMES[number]) {
        resolve(window.MUSOKU_VOLUMES[number]);
        return;
      }
      const entry = volumeManifest[number];
      if (!entry || !entry.file) {
        reject(new Error(`No data for volume ${number}`));
        return;
      }
      const script = document.createElement("script");
      script.src = entry.file;
      script.onload = () => {
        if (store[number]) {
          resolve(store[number]);
        } else {
          reject(new Error(`Volume ${number} loaded without data`));
        }
      };
      script.onerror = () => reject(new Error(`Could not load ${entry.file}`));
      document.head.appendChild(script);
    });
  }

  const SPEAKER_HUES = {
    Rudeus: [26, 45],
    Orsted: [218, 28],
    Eris: [350, 52],
    Nanahoshi: [272, 32],
    Roxy: [228, 48],
    Sylphiette: [148, 34],
    "Man-God": [40, 58],
    Nina: [8, 57],
    Aisha: [18, 48],
    Norn: [204, 26],
    Ghislaine: [24, 31],
    Isolde: [310, 25],
    Lilia: [332, 26],
    Cliff: [45, 48],
    Elinalise: [322, 42],
    Zanoba: [264, 36],
    Gall: [0, 38],
    Reida: [34, 27],
    Georg: [220, 17],
    Richard: [42, 52],
    Arumanfi: [50, 62],
    Courier: [30, 33],
    "Drug Dealer": [105, 23],
    "Elf Artisan": [170, 26],
    Guard: [210, 12],
    "Mercenary Bodyguard": [4, 13],
    Perugius: [258, 30],
    Sylvaril: [282, 32],
    "Wise Old Hermit": [260, 20],
    Zenith: [188, 30],
    Luke: [212, 38],
    Ariel: [318, 44],
    "Ariel Anemoi Asura": [318, 44],
    Lucie: [345, 34],
    Sieg: [190, 36],
    "Siegfried Saladin Greyrat": [190, 36],
    Grabel: [12, 24],
    Darius: [208, 18],
    Pilemon: [44, 26],
    Cleane: [300, 22],
    Lienhard: [38, 46],
    Gertrude: [280, 26],
    Ruquag: [150, 24],
    "Ruquag Mire": [150, 24],
    "Tal-Chi": [82, 34],
    Gino: [330, 24],
    Sara: [350, 36],
    Atofe: [10, 32],
    Moore: [200, 18],
    "Student Council President": [318, 38],
  };

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (character) => {
      switch (character) {
        case "&":
          return "&amp;";
        case "<":
          return "&lt;";
        case ">":
          return "&gt;";
        case '"':
          return "&quot;";
        case "'":
          return "&#39;";
        default:
          return character;
      }
    });
  }

  function formatNumber(value) {
    return numberFormatter.format(Number(value) || 0);
  }

  function volumeLabel(volumeNumber = data.meta.volume) {
    return `Volume ${volumeNumber}`;
  }

  function assetUrl(filename) {
    const base = data.meta.assetBase || `images/vol${data.meta.volume}`;
    return `${base}/${encodeURIComponent(filename)}`;
  }

  function volumeStorageKey(name, volume = data.meta.volume) {
    return `mt15:v${volume}:${name}`;
  }

  function chapterNumber(chapter) {
    if (chapter.kind === "extra") return "EX";
    if (chapter.kind === "diary") return "D";
    if (chapter.kind === "interlude") return "IL";
    if (chapter.kind === "story") return `S${chapter.number}`;
    if (chapter.kind === "appendix") return "AP";
    if (chapter.kind === "afterword") return "AW";
    if (chapter.kind === "epilogue") return "EP";
    return String(chapter.number).padStart(2, "0");
  }

  function chapterKicker(chapter) {
    if (chapter.kind === "extra") return "Extra Chapter";
    if (chapter.kind === "diary") return "Diary";
    if (chapter.kind === "interlude") return "Interlude";
    if (chapter.kind === "story") return `Story ${chapter.number}`;
    if (chapter.kind === "appendix") return "Appendix";
    if (chapter.kind === "afterword") return "Afterword";
    if (chapter.kind === "epilogue") return "Epilogue";
    return `Chapter ${chapter.number}`;
  }

  function chapterTitle(chapter) {
    return chapter.kind === "extra"
      ? chapter.title.replace(/^Extra Chapter:\s*/, "")
      : chapter.title;
  }

  function chapterShortLabel(chapter) {
    return `${chapterKicker(chapter)} · ${chapterTitle(chapter)}`;
  }

  function speakerStyle(name) {
    const hue = SPEAKER_HUES[name] || fallbackHue(name);
    return `--speaker-h:${hue[0]};--speaker-s:${hue[1]}%;`;
  }

  function fallbackHue(name) {
    let hash = 0;
    for (const character of String(name)) {
      hash = (hash * 31 + character.codePointAt(0)) % 360;
    }
    return [hash, 32];
  }

  function blockContent(block) {
    return block.html || escapeHtml(block.text);
  }

  function speakerTag(block) {
    if (block.mixed || block.embeddedDialogue) return "quoted";
    if (block.recollection) return "remembered";
    if (block.imagined) return "imagined";
    return "";
  }

  function renderSpeaker(block) {
    if (!block.speaker) return "";
    const confidence =
      block.speakerConfidence === "medium"
        ? ' data-confidence="medium" title="Speaker inferred from context"'
        : "";
    const tag = speakerTag(block);
    return `
      <div class="speaker" style="${speakerStyle(block.speaker)}"${confidence}>
        <span class="speaker__dot" aria-hidden="true"></span>
        <span class="speaker__name">${escapeHtml(block.speaker)}</span>
        ${tag ? `<span class="speaker__tag">${tag}</span>` : ""}
      </div>`;
  }

  function renderBlock(block) {
    const classes = ["block", `block--${block.type}`];
    if (block.mixed) classes.push("block--mixed");
    if (block.recollection) classes.push("block--recollection");
    if (block.imagined) classes.push("block--imagined");
    if (block.embeddedDialogue) classes.push("block--embedded");
    if (block.speaker) classes.push("has-speaker");

    const id = escapeHtml(block.id);
    const speaker = renderSpeaker(block);

    if (block.type === "spacer") {
      return `<div class="${classes.join(" ")}" data-block-id="${id}" aria-hidden="true"></div>`;
    }

    if (block.type === "silence") {
      const silence = String(block.text || "").replace(/[“”"]/g, "") || "…";
      return `
        <div class="${classes.join(" ")}" data-block-id="${id}" role="separator" aria-label="Silence">
          <span>${escapeHtml(silence)}</span>
        </div>`;
    }

    if (block.type === "inscription") {
      return `<div class="${classes.join(" ")}" data-block-id="${id}">${blockContent(block)}</div>`;
    }

    return `
      <div class="${classes.join(" ")}" data-block-id="${id}"${block.speaker ? ` data-speaker="${escapeHtml(block.speaker)}"` : ""}>
        ${speaker}
        <div class="block__body"><p>${blockContent(block)}</p></div>
      </div>`;
  }

  function renderDocument(type, group) {
    const label = type === "diary" ? "From the diary" : "Letter";
    const body = group
      .map((block) =>
        block.type === "spacer"
          ? '<div class="document__gap" aria-hidden="true"></div>'
          : `<p data-block-id="${escapeHtml(block.id)}">${blockContent(block)}</p>`
      )
      .join("");

    return `
      <div class="document document--${type}" data-document="${type}">
        <div class="document__header">
          <span>${label}</span>
          <span class="document__line" aria-hidden="true"></span>
        </div>
        <div class="document__body">${body}</div>
      </div>`;
  }

  function renderBlocks(blocks) {
    const output = [];
    let index = 0;

    while (index < blocks.length) {
      const block = blocks[index];

      if (block.type === "spacer") {
        output.push(renderBlock(block));
        index += 1;
        continue;
      }

      if (block.type === "diary" || block.type === "letter") {
        const type = block.type;
        const group = [];
        let cursor = index;

        while (cursor < blocks.length) {
          if (blocks[cursor].type === type) {
            group.push(blocks[cursor]);
            cursor += 1;
            continue;
          }

          if (blocks[cursor].type === "spacer") {
            let lookahead = cursor;
            while (lookahead < blocks.length && blocks[lookahead].type === "spacer") {
              lookahead += 1;
            }
            if (lookahead < blocks.length && blocks[lookahead].type === type) {
              for (; cursor < lookahead; cursor += 1) group.push(blocks[cursor]);
              continue;
            }
          }

          break;
        }

        output.push(renderDocument(type, group));
        index = cursor;
        continue;
      }

      output.push(renderBlock(block));
      index += 1;
    }

    return output.join("");
  }

  function renderScene(scene) {
    const cast = (scene.cast || []).map(escapeHtml).join(" · ");
    const location = escapeHtml(scene.location || "");
    const header =
      location || cast
        ? `<header class="scene-header">
             ${location ? `<span class="scene-location">${location}</span>` : ""}
             ${cast ? `<span class="scene-cast">${cast}</span>` : ""}
           </header>`
        : "";

    return `
      <section class="scene" id="${escapeHtml(scene.id)}" data-scene-id="${escapeHtml(scene.id)}">
        ${header}
        <div class="blocks">${renderBlocks(scene.blocks)}</div>
      </section>`;
  }

  function renderChapterArt(chapter) {
    const images = chapter.images || [];
    if (!images.length) return "";

    const figures = images
      .map((image) => {
        const alt = image.alt || `Illustration from ${chapterTitle(chapter)}`;
        return `
          <figure>
            <img src="${assetUrl(image.src)}"
                 width="1403" height="2000"
                 loading="lazy" decoding="async"
                 alt="${escapeHtml(alt)}">
            <figcaption>Illustration</figcaption>
          </figure>`;
      })
      .join("");

    return `<div class="chapter-art${images.length > 1 ? " chapter-art--multi" : ""}">${figures}</div>`;
  }

  function renderChapter(chapter) {
    const title = chapterTitle(chapter);
    const headingId = `${chapter.id}-title`;
    const scenes = chapter.scenes.map(renderScene).join("");

    return `
      <section class="chapter" id="${escapeHtml(chapter.id)}" data-chapter-id="${escapeHtml(chapter.id)}" aria-labelledby="${headingId}">
        <header class="chapter-header" data-number="${chapterNumber(chapter)}">
          <p class="chapter-kicker">${chapterKicker(chapter)}</p>
          <h2 id="${headingId}">${escapeHtml(title)}</h2>
          <div class="chapter-meta">
            <span class="meta-pill">POV ${escapeHtml(chapter.pov)}</span>
            <span>${formatNumber(chapter.wordCount)} words</span>
            <span>${chapter.sceneCount} ${chapter.sceneCount === 1 ? "scene" : "scenes"}</span>
          </div>
        </header>
        ${renderChapterArt(chapter)}
        ${scenes}
      </section>`;
  }

  function renderToc() {
    toc.innerHTML = data.chapters
      .map((chapter) => {
        const number = chapterNumber(chapter);
        return `
          <a class="toc__item" href="#${escapeHtml(chapter.id)}" data-chapter-link="${escapeHtml(chapter.id)}">
            <span class="toc__num">${number}</span>
            <span>
              <span class="toc__title">${escapeHtml(chapterTitle(chapter))}</span>
              <span class="toc__meta">${formatNumber(chapter.wordCount)} words · ${escapeHtml(chapter.pov)}</span>
            </span>
          </a>`;
      })
      .join("");
  }

  function renderVolumeStats() {
    const stats = data.stats || {};
    const fields = {
      chapters: stats.chapters ?? data.chapters.length,
      words: stats.words ?? 0,
      speakers: stats.speakers ?? (data.speakers || []).length,
    };
    document.querySelectorAll("[data-stat]").forEach((element) => {
      const key = element.getAttribute("data-stat");
      if (key in fields) {
        element.textContent = key === "words" ? formatNumber(fields[key]) : fields[key];
      }
    });
  }

  function renderVolumeNav() {
    if (!volumeButtons) return;
    volumeButtons.innerHTML = volumeOrder
      .map((number) => {
        const entry = volumeManifest[number] || {};
        const label = entry.title
          ? `Volume ${number}: ${entry.title.replace(/^.*Vol\.\s*/, "")}`
          : `Volume ${number}`;
        return `
          <button class="volume-nav__button" type="button" data-volume="${number}"
                  aria-pressed="${number === activeVolume ? "true" : "false"}"
                  aria-label="${escapeHtml(label)}" title="${escapeHtml(label)}">${number}</button>`;
      })
      .join("");
  }

  function renderVolumeMetadata() {
    const number = data.meta.volume;
    const label = volumeLabel();
    const cover = assetUrl("CoverDesign.jpg");
    document.title = `Mushoku Tensei — ${label} Reader`;
    if (metaDescription) {
      metaDescription.content = `A scrolling reader edition of Mushoku Tensei: Jobless Reincarnation ${label}, with speaker-labeled dialogue.`;
    }
    if (sidebarVolume) sidebarVolume.textContent = label;
    if (sidebarCover) {
      sidebarCover.src = cover;
      sidebarCover.alt = `Cover of ${data.meta.title || label}`;
    }
    if (heroVolume) heroVolume.textContent = String(number);
    if (heroLede) heroLede.textContent = data.meta.blurb || "A scrolling reader edition.";
    if (heroCover) {
      heroCover.src = cover;
      heroCover.alt = `Cover of ${data.meta.title || label}`;
    }
    if (volumeEndTitle) volumeEndTitle.textContent = label;
    if (beginReading && data.chapters.length) {
      beginReading.href = `#${data.chapters[0].id}`;
    }
    if (focusChapterTitle) focusChapterTitle.textContent = label;
    if (timeline) timeline.setAttribute("aria-label", `Scenes in ${label}`);
  }

  function renderCurrentVolume() {
    renderVolumeMetadata();
    renderVolumeNav();
    renderToc();
    chaptersRoot.innerHTML = data.chapters.map(renderChapter).join("");
    renderVolumeStats();
    rebuildSceneItems();
    buildTimeline();

    chapterSections = Array.from(chaptersRoot.querySelectorAll(".chapter"));
    tocLinks = new Map(
      Array.from(toc.querySelectorAll("[data-chapter-link]")).map((link) => [
        link.dataset.chapterLink,
        link,
      ])
    );
    currentSceneIndex = 0;
    updateScrollUi();
  }

  function volumeFromUrl() {
    try {
      const requested = Number(
        new URLSearchParams(window.location.search).get("volume")
      );
      return volumeOrder.includes(requested) ? requested : null;
    } catch {
      return null;
    }
  }

  function updateUrlForVolume(number) {
    try {
      const url = new URL(window.location.href);
      url.searchParams.set("volume", String(number));
      url.hash = "";
      history.replaceState(null, "", url.pathname + url.search);
    } catch {
      /* Some file:// contexts restrict history updates; switching still works. */
    }
  }

  function switchVolume(volumeNumber) {
    const number = Number(volumeNumber);
    if (!volumeManifest[number]) return;
    if (data && number === data.meta.volume) return;
    if (switchingVolume) return;
    switchingVolume = true;

    const finish = () => {
      switchingVolume = false;
    };

    if (focusOpen) closeFocus();
    if (settingsOpen) closeSettings();
    if (data) saveCurrentScroll();

    const targetScroll =
      Number(storage.get(volumeStorageKey("scroll", number))) ||
      (number === 15 ? Number(storage.get("mt15:scroll")) || 0 : 0);

    loadVolumeData(number)
      .then((volumeData) => {
        data = volumeData;
        activeVolume = number;
        storage.set("mt15:last-volume", String(number));
        closeNav();
        updateUrlForVolume(number);
        renderCurrentVolume();
        jumpTo(targetScroll > 240 ? targetScroll : 0);
        updateScrollUi();
        finish();
      })
      .catch(() => {
        finish();
        showToast("That volume could not be loaded.");
      });
  }

  if (volumeButtons) {
    volumeButtons.addEventListener("click", (event) => {
      const button = event.target.closest("[data-volume]");
      if (button) switchVolume(Number(button.dataset.volume));
    });
  }

  // ---------------------------------------------------------------------
  // Reading preferences
  // ---------------------------------------------------------------------

  const SETTINGS_DEFAULTS = {
    typeface: "serif",
    lineHeight: "cozy",
    width: "standard",
    alignment: "justify",
  };
  const SETTINGS_STORAGE_KEYS = {
    typeface: "mt15:typeface",
    lineHeight: "mt15:line-height",
    width: "mt15:width",
    alignment: "mt15:alignment",
  };

  function storedChoice(key, allowed, fallback) {
    const value = storage.get(key);
    return allowed.includes(value) ? value : fallback;
  }

  const settings = {
    typeface: storedChoice(
      SETTINGS_STORAGE_KEYS.typeface,
      TYPEFACE_VALUES,
      SETTINGS_DEFAULTS.typeface
    ),
    lineHeight: storedChoice(
      SETTINGS_STORAGE_KEYS.lineHeight,
      Object.keys(LINE_HEIGHT_VALUES),
      SETTINGS_DEFAULTS.lineHeight
    ),
    width: storedChoice(
      SETTINGS_STORAGE_KEYS.width,
      Object.keys(READING_WIDTH_VALUES),
      SETTINGS_DEFAULTS.width
    ),
    alignment: storedChoice(
      SETTINGS_STORAGE_KEYS.alignment,
      ["justify", "left"],
      SETTINGS_DEFAULTS.alignment
    ),
  };

  let settingsOpen = false;
  let settingsReturnFocus = null;
  let settingsInertTarget = null;

  function updateSettingsUi() {
    if (settingsFontValue) {
      settingsFontValue.textContent = `${fontSize} px`;
    }

    settingsPanel.querySelectorAll("[data-setting]").forEach((button) => {
      const key = button.dataset.setting;
      const value = button.dataset.value;
      const current = key === "theme" ? root.dataset.theme : settings[key];
      button.setAttribute("aria-pressed", value === current ? "true" : "false");
    });
  }

  function applySettings() {
    root.dataset.typeface = settings.typeface;
    root.style.setProperty(
      "--reader-line-height",
      LINE_HEIGHT_VALUES[settings.lineHeight]
    );
    root.style.setProperty(
      "--reading-width",
      READING_WIDTH_VALUES[settings.width]
    );
    root.style.setProperty("--narration-align", settings.alignment);
    updateSettingsUi();
  }

  // ---------------------------------------------------------------------
  // Fullscreen scene reader
  // ---------------------------------------------------------------------

  let sceneItems = [];

  function rebuildSceneItems() {
    sceneItems = [];
    data.chapters.forEach((chapter, chapterIndex) => {
      chapter.scenes.forEach((scene, sceneIndex) => {
        sceneItems.push({
          chapter,
          chapterIndex,
          scene,
          sceneIndex,
          sceneCount: chapter.scenes.length,
          globalIndex: sceneItems.length,
        });
      });
    });
  }

  let focusOpen = false;
  let currentSceneIndex = 0;
  let focusEnteredScene = 0;
  let focusOriginalScroll = 0;
  let focusReturnFocus = null;
  let timelineTicks = [];
  let timelineChapterEls = [];
  let timelineFill = null;

  function renderFocusScene(item) {
    const scene = item.scene;
    const location = escapeHtml(scene.location || "Unnamed scene");
    const cast = (scene.cast || []).map(escapeHtml).join(" · ");
    const chapterLabel = `${chapterKicker(item.chapter)} · ${chapterTitle(item.chapter)}`;
    const hasNext = item.globalIndex < sceneItems.length - 1;
    const endAction = hasNext
      ? '<button class="button button--quiet focus-next-inline" type="button">Next scene <span aria-hidden="true">→</span></button>'
      : '<span class="focus-scene__end-note">End of volume</span>';

    return `
      <article class="focus-scene" data-focus-scene-id="${escapeHtml(scene.id)}">
        <header class="focus-scene__header">
          <p class="focus-scene__chapter">${escapeHtml(chapterLabel)}</p>
          <p class="focus-scene__number">Scene ${item.sceneIndex + 1} of ${item.sceneCount}</p>
          <h3 class="focus-scene__location">${location}</h3>
          ${cast ? `<p class="focus-scene__cast">${cast}</p>` : ""}
        </header>
        <div class="blocks">${renderBlocks(scene.blocks)}</div>
        <footer class="focus-scene__end">
          <span>End of scene</span>
          ${endAction}
        </footer>
      </article>`;
  }

  function buildTimeline() {
    timeline.style.setProperty("--scene-count", String(sceneItems.length));

    const chapterLabels = data.chapters
      .map((chapter, chapterIndex) => {
        const span = chapter.scenes.length;
        const label = `${chapterKicker(chapter)} — ${chapterTitle(chapter)}`;
        return `<div class="timeline__chapter" data-timeline-chapter="${chapterIndex}" style="grid-column: span ${span}" title="${escapeHtml(label)}">${chapterNumber(chapter)}</div>`;
      })
      .join("");

    const ticks = sceneItems
      .map((item) => {
        const label = `${chapterKicker(item.chapter)} · Scene ${item.sceneIndex + 1}: ${item.scene.location || "Scene"}`;
        return `<button class="timeline__tick" type="button" data-scene-index="${item.globalIndex}" title="${escapeHtml(label)}" aria-label="${escapeHtml(label)}"><span class="timeline__dot" aria-hidden="true"></span></button>`;
      })
      .join("");

    timeline.innerHTML = `
      <div class="timeline__chapters">${chapterLabels}</div>
      <div class="timeline__track" id="timelineTrack">
        <div class="timeline__rail" aria-hidden="true"></div>
        <div class="timeline__fill" aria-hidden="true"></div>
        ${ticks}
      </div>`;

    timelineTicks = Array.from(timeline.querySelectorAll(".timeline__tick"));
    timelineChapterEls = Array.from(
      timeline.querySelectorAll("[data-timeline-chapter]")
    );
    timelineFill = timeline.querySelector(".timeline__fill");

    const track = timeline.querySelector(".timeline__track");
    track.addEventListener("click", (event) => {
      const tick = event.target.closest(".timeline__tick");
      if (tick) {
        showFocusScene(Number(tick.dataset.sceneIndex));
        return;
      }

      const rect = track.getBoundingClientRect();
      const ratio = (event.clientX - rect.left) / rect.width;
      const index = Math.max(
        0,
        Math.min(sceneItems.length - 1, Math.floor(ratio * sceneItems.length))
      );
      showFocusScene(index);
    });
  }

  function showFocusScene(index) {
    if (!sceneItems.length) return;

    currentSceneIndex = Math.max(0, Math.min(sceneItems.length - 1, index));
    const item = sceneItems[currentSceneIndex];

    focusChapterKicker.textContent = `${chapterKicker(item.chapter)} · Scene ${item.sceneIndex + 1} of ${item.sceneCount}`;
    focusChapterTitle.textContent = chapterTitle(item.chapter);
    focusSceneMeta.textContent = item.scene.location || "";
    focusMain.innerHTML = renderFocusScene(item);
    focusMain.scrollTop = 0;
    focusStatus.textContent = `Scene ${currentSceneIndex + 1} of ${sceneItems.length}`;
    focusPrev.disabled = currentSceneIndex === 0;
    focusNext.disabled = currentSceneIndex === sceneItems.length - 1;

    timelineTicks.forEach((tick, tickIndex) => {
      const isActive = tickIndex === currentSceneIndex;
      tick.classList.toggle("is-active", isActive);
      if (isActive) tick.setAttribute("aria-current", "step");
      else tick.removeAttribute("aria-current");
    });

    timelineChapterEls.forEach((label, chapterIndex) => {
      label.classList.toggle("is-active", chapterIndex === item.chapterIndex);
    });

    if (timelineFill) {
      timelineFill.style.width = `${((currentSceneIndex + 0.5) / sceneItems.length) * 100}%`;
    }

    storage.set(volumeStorageKey("focus-scene"), String(currentSceneIndex));

    const activeTick = timelineTicks[currentSceneIndex];
    if (activeTick) {
      window.requestAnimationFrame(() => {
        const scrollerRect = timelineScroller.getBoundingClientRect();
        const tickRect = activeTick.getBoundingClientRect();
        if (
          tickRect.left < scrollerRect.left + 24 ||
          tickRect.right > scrollerRect.right - 24
        ) {
          activeTick.scrollIntoView({
            block: "nearest",
            inline: "center",
            behavior: reducedMotion ? "auto" : "smooth",
          });
        }
      });
    }
  }

  function currentSceneFromScroll() {
    if (!sceneItems.length) return 0;

    const marker = window.scrollY + Math.min(220, window.innerHeight * 0.3);
    let chapterIndex = 0;

    if (chapterSections.length) {
      chapterSections.forEach((section, sectionIndex) => {
        if (
          section.getBoundingClientRect().top + window.scrollY <=
          marker
        ) {
          chapterIndex = sectionIndex;
        }
      });
    } else {
      data.chapters.forEach((chapter, index) => {
        const element = document.getElementById(chapter.id);
        if (
          element &&
          element.getBoundingClientRect().top + window.scrollY <= marker
        ) {
          chapterIndex = index;
        }
      });
    }

    const chapterSceneItems = sceneItems.filter(
      (item) => item.chapterIndex === chapterIndex
    );
    let index = chapterSceneItems.length
      ? chapterSceneItems[0].globalIndex
      : 0;

    chapterSceneItems.forEach((item) => {
      const element = document.getElementById(item.scene.id);
      if (
        element &&
        element.getBoundingClientRect().top + window.scrollY <= marker
      ) {
        index = item.globalIndex;
      }
    });

    return index;
  }

  function setChromeHidden(hidden) {
    if (!focusOpen) return;

    const shouldHide = Boolean(hidden);
    focusReader.classList.toggle("chrome-hidden", shouldHide);
    focusChromeToggle.setAttribute(
      "aria-expanded",
      shouldHide ? "false" : "true"
    );

    const active = document.activeElement;
    const header = focusReader.querySelector(".focus-header");
    const footer = focusReader.querySelector(".focus-timeline");

    if (
      active &&
      ((header && header.contains(active)) || (footer && footer.contains(active)))
    ) {
      focusMain.focus({ preventScroll: true });
    } else if (!shouldHide) {
      focusMain.focus({ preventScroll: true });
    }
  }

  function updateFullscreenButton() {
    const active = Boolean(document.fullscreenElement);
    focusFullscreen.setAttribute("aria-pressed", active ? "true" : "false");
    focusFullscreen.setAttribute(
      "aria-label",
      active ? "Exit fullscreen" : "Enter fullscreen"
    );
    focusFullscreen.setAttribute(
      "title",
      active ? "Exit fullscreen" : "Enter fullscreen"
    );
    focusFullscreen.textContent = active ? "⤡" : "⛶";

    if (focusOpen) {
      setChromeHidden(active);
    }
  }

  function openFocus() {
    if (focusOpen) return;
    if (settingsOpen) closeSettings();

    const start = currentSceneFromScroll();
    focusReturnFocus = document.activeElement;
    closeNav();
    focusOpen = true;
    focusEnteredScene = start;
    focusOriginalScroll = window.scrollY;
    currentSceneIndex = start;

    focusReader.hidden = false;
    focusReader.classList.remove("chrome-hidden");
    focusChromeToggle.setAttribute("aria-expanded", "true");
    document.body.classList.add("focus-open");
    if (appRoot) {
      appRoot.inert = true;
      appRoot.setAttribute("aria-hidden", "true");
    }

    showFocusScene(start);
    focusMain.focus({ preventScroll: true });
    updateFullscreenButton();

    if (
      typeof focusReader.requestFullscreen === "function" &&
      !document.fullscreenElement
    ) {
      focusReader.requestFullscreen().catch(() => {
        /* The full-viewport overlay still works without native fullscreen. */
      });
    }
  }

  function closeFocus() {
    if (!focusOpen) return;
    if (settingsOpen) closeSettings();

    const item = sceneItems[currentSceneIndex];
    focusOpen = false;
    focusReader.hidden = true;
    focusReader.classList.remove("chrome-hidden");
    document.body.classList.remove("focus-open");
    if (appRoot) {
      appRoot.inert = false;
      appRoot.removeAttribute("aria-hidden");
    }

    if (document.fullscreenElement) {
      document.exitFullscreen().catch(() => {});
    }

    if (currentSceneIndex !== focusEnteredScene && item) {
      const target = document.getElementById(item.scene.id);
      if (target) {
        jumpTo(target.getBoundingClientRect().top + window.scrollY - 82);
      } else {
        jumpTo(focusOriginalScroll);
      }
    } else {
      jumpTo(focusOriginalScroll);
    }
    updateScrollUi();

    const returnTarget =
      focusReturnFocus &&
      focusReturnFocus !== document.body &&
      focusReturnFocus.isConnected
        ? focusReturnFocus
        : openFocusButton;
    if (returnTarget && typeof returnTarget.focus === "function") {
      returnTarget.focus({ preventScroll: true });
    }
  }

  function trapFocus(event) {
    if (event.key !== "Tab") return;
    const focusables = Array.from(
      focusReader.querySelectorAll(
        'button:not([disabled]), [href], [tabindex]:not([tabindex="-1"])'
      )
    ).filter((element) => element.offsetParent !== null);

    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  if (openFocusButton) openFocusButton.addEventListener("click", openFocus);
  if (openFocusHeroButton) openFocusHeroButton.addEventListener("click", openFocus);
  focusClose.addEventListener("click", closeFocus);
  focusChromeToggle.addEventListener("click", () => setChromeHidden(true));
  focusChromeReveal.addEventListener("click", () => setChromeHidden(false));
  focusPrev.addEventListener("click", () => showFocusScene(currentSceneIndex - 1));
  focusNext.addEventListener("click", () => showFocusScene(currentSceneIndex + 1));
  focusReader.addEventListener("keydown", trapFocus);

  focusMain.addEventListener("click", (event) => {
    if (event.target.closest(".focus-next-inline")) {
      showFocusScene(currentSceneIndex + 1);
      focusMain.focus({ preventScroll: true });
    }
  });

  focusFullscreen.addEventListener("click", () => {
    if (document.fullscreenElement) {
      document.exitFullscreen().catch(() => {});
    } else if (typeof focusReader.requestFullscreen === "function") {
      focusReader.requestFullscreen().catch(() => {});
    }
  });

  document.addEventListener("fullscreenchange", updateFullscreenButton);

  if (!document.fullscreenEnabled) {
    focusFullscreen.hidden = true;
  }

  // ---------------------------------------------------------------------
  // Reading settings panel
  // ---------------------------------------------------------------------

  function setSettingsExpanded(expanded) {
    [settingsToggle, focusSettingsToggle].forEach((button) => {
      if (button) button.setAttribute("aria-expanded", expanded ? "true" : "false");
    });
  }

  function openSettings() {
    if (settingsOpen) return;

    settingsOpen = true;
    settingsReturnFocus = document.activeElement;
    settingsInertTarget = focusOpen ? focusReader : appRoot;
    if (settingsInertTarget) settingsInertTarget.inert = true;

    settingsPanel.hidden = false;
    settingsScrim.hidden = false;
    document.body.classList.add("settings-open");
    setSettingsExpanded(true);
    updateSettingsUi();
    settingsPanel.focus({ preventScroll: true });
  }

  function closeSettings() {
    if (!settingsOpen) return;

    settingsOpen = false;
    settingsPanel.hidden = true;
    settingsScrim.hidden = true;
    document.body.classList.remove("settings-open");
    setSettingsExpanded(false);

    if (settingsInertTarget) {
      settingsInertTarget.inert = false;
      settingsInertTarget = null;
    }

    const returnTarget =
      settingsReturnFocus &&
      settingsReturnFocus !== document.body &&
      settingsReturnFocus.isConnected
        ? settingsReturnFocus
        : focusOpen
          ? focusSettingsToggle
          : settingsToggle;

    if (returnTarget && typeof returnTarget.focus === "function") {
      returnTarget.focus({ preventScroll: true });
    }
  }

  function trapSettingsFocus(event) {
    if (event.key !== "Tab") return;
    const focusables = Array.from(
      settingsPanel.querySelectorAll(
        'button:not([disabled]), [href], [tabindex]:not([tabindex="-1"])'
      )
    ).filter((element) => element.offsetParent !== null);

    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];

    if (document.activeElement === settingsPanel) {
      event.preventDefault();
      (event.shiftKey ? last : first).focus();
    } else if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  [settingsToggle, focusSettingsToggle].forEach((button) => {
    if (!button) return;
    button.setAttribute("aria-expanded", "false");
    button.addEventListener("click", () => {
      if (settingsOpen) closeSettings();
      else openSettings();
    });
  });

  settingsClose.addEventListener("click", closeSettings);
  settingsScrim.addEventListener("click", closeSettings);
  settingsPanel.addEventListener("keydown", trapSettingsFocus);

  settingsPanel.addEventListener("click", (event) => {
    const button = event.target.closest("[data-setting]");
    if (!button) return;

    const key = button.dataset.setting;
    const value = button.dataset.value;

    if (key === "theme") {
      applyTheme(value);
      storage.set("mt15:theme", value);
      updateSettingsUi();
      return;
    }

    if (!(key in settings)) return;
    settings[key] = value;
    storage.set(SETTINGS_STORAGE_KEYS[key], value);
    applySettings();
  });

  settingsReset.addEventListener("click", () => {
    Object.assign(settings, SETTINGS_DEFAULTS);
    Object.entries(SETTINGS_STORAGE_KEYS).forEach(([key, storageKey]) => {
      storage.set(storageKey, settings[key]);
    });
    applyTheme("light");
    storage.set("mt15:theme", "light");
    fontSize = setFontSize(FONT_DEFAULT);
    applySettings();
  });

  document.addEventListener("click", (event) => {
    if (!settingsOpen) return;
    if (
      settingsPanel.contains(event.target) ||
      settingsToggle.contains(event.target) ||
      (focusSettingsToggle && focusSettingsToggle.contains(event.target))
    ) {
      return;
    }
    closeSettings();
  });

  // ---------------------------------------------------------------------
  // Theme and type size
  // ---------------------------------------------------------------------

  const themeButtons = [themeToggle, focusThemeToggle].filter(Boolean);
  const fontDecreaseButtons = [
    fontDecrease,
    focusFontDecrease,
    settingsFontDecrease,
  ].filter(Boolean);
  const fontIncreaseButtons = [
    fontIncrease,
    focusFontIncrease,
    settingsFontIncrease,
  ].filter(Boolean);

  function applyTheme(theme) {
    root.dataset.theme = theme;
    const isDark = theme === "dark";
    themeButtons.forEach((button) => {
      button.innerHTML = isDark ? SUN_ICON : MOON_ICON;
      button.setAttribute(
        "aria-label",
        isDark ? "Switch to light theme" : "Switch to dark theme"
      );
      button.setAttribute(
        "title",
        isDark ? "Switch to light theme" : "Switch to dark theme"
      );
    });
    updateSettingsUi();
  }

  function setFontSize(value) {
    const size = Math.max(FONT_MIN, Math.min(FONT_MAX, value));
    root.style.setProperty("--reader-font-size", `${size}px`);
    fontDecreaseButtons.forEach((button) => {
      button.disabled = size <= FONT_MIN;
    });
    fontIncreaseButtons.forEach((button) => {
      button.disabled = size >= FONT_MAX;
    });
    if (settingsFontValue) settingsFontValue.textContent = `${size} px`;
    storage.set("mt15:font-size", String(size));
    return size;
  }

  function toggleTheme() {
    const next = root.dataset.theme === "dark" ? "light" : "dark";
    applyTheme(next);
    storage.set("mt15:theme", next);
  }

  let fontSize = Number(storage.get("mt15:font-size")) || FONT_DEFAULT;
  applyTheme(storage.get("mt15:theme") || "light");
  fontSize = setFontSize(fontSize);
  applySettings();

  themeButtons.forEach((button) => {
    button.addEventListener("click", toggleTheme);
  });

  fontDecreaseButtons.forEach((button) => {
    button.addEventListener("click", () => {
      fontSize = setFontSize(fontSize - 1);
    });
  });

  fontIncreaseButtons.forEach((button) => {
    button.addEventListener("click", () => {
      fontSize = setFontSize(fontSize + 1);
    });
  });

  // ---------------------------------------------------------------------
  // Mobile contents drawer
  // ---------------------------------------------------------------------

  function openNav() {
    document.body.classList.add("nav-open");
    menuToggle.setAttribute("aria-expanded", "true");
    menuToggle.setAttribute("aria-label", "Close contents");
    sidebar.focus({ preventScroll: true });
  }

  function closeNav() {
    const wasOpen = document.body.classList.contains("nav-open");
    document.body.classList.remove("nav-open");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Open contents");
    if (wasOpen && window.matchMedia("(max-width: 1000px)").matches) {
      menuToggle.focus({ preventScroll: true });
    }
  }

  menuToggle.addEventListener("click", () => {
    if (document.body.classList.contains("nav-open")) {
      closeNav();
    } else {
      openNav();
    }
  });

  sidebarOverlay.addEventListener("click", closeNav);

  toc.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeNav();
  });

  sidebar.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeNav();
  });

  // ---------------------------------------------------------------------
  // Scroll position, progress, and current chapter
  // ---------------------------------------------------------------------

  let chapterSections = [];
  let tocLinks = new Map();
  let ticking = false;
  let saveTimer = null;

  function saveCurrentScroll() {
    storage.set(
      volumeStorageKey("scroll"),
      String(Math.max(0, Math.round(window.scrollY)))
    );
  }

  function updateScrollUi() {
    const scrollY = window.scrollY;
    const viewport = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    const maxScroll = Math.max(0, documentHeight - viewport);
    const progress = maxScroll > 0 ? Math.min(1, Math.max(0, scrollY / maxScroll)) : 0;
    progressBar.style.width = `${(progress * 100).toFixed(2)}%`;

    const hero = document.querySelector(".hero");
    const heroBottom = hero
      ? hero.getBoundingClientRect().bottom + scrollY
      : 0;
    const marker = scrollY + Math.min(160, viewport * 0.22);
    let active = null;

    if (marker >= heroBottom) {
      for (const section of chapterSections) {
        const top = section.getBoundingClientRect().top + scrollY;
        if (top <= marker) active = section;
      }
    }

    const activeId = active ? active.dataset.chapterId : null;
    tocLinks.forEach((link, id) => {
      link.classList.toggle("is-active", id === activeId);
    });

    if (active) {
      const chapter = data.chapters.find((item) => item.id === activeId);
      currentChapter.textContent = chapter ? chapterShortLabel(chapter) : volumeLabel();
    } else {
      currentChapter.textContent = volumeLabel();
    }

    backToTop.classList.toggle("is-visible", scrollY > 900);

    clearTimeout(saveTimer);
    saveTimer = window.setTimeout(saveCurrentScroll, 220);
  }

  function requestScrollUpdate() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(() => {
      ticking = false;
      updateScrollUi();
    });
  }

  function jumpTo(top) {
    const previous = root.style.scrollBehavior;
    root.style.scrollBehavior = "auto";
    window.scrollTo(0, Math.max(0, top));
    root.style.scrollBehavior = previous;
  }

  window.addEventListener("scroll", requestScrollUpdate, { passive: true });
  window.addEventListener("resize", requestScrollUpdate);

  backToTop.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: reducedMotion ? "auto" : "smooth",
    });
  });

  // ---------------------------------------------------------------------
  // Toast
  // ---------------------------------------------------------------------

  let toastTimer = null;

  function hideToast() {
    toast.hidden = true;
    toast.innerHTML = "";
  }

  function showToast(message, actionLabel, action) {
    toast.innerHTML = `<span>${escapeHtml(message)}</span>`;

    if (actionLabel && action) {
      const actionButton = document.createElement("button");
      actionButton.type = "button";
      actionButton.textContent = actionLabel;
      actionButton.addEventListener("click", () => {
        action();
        hideToast();
      });
      toast.appendChild(actionButton);
    }

    toast.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = window.setTimeout(hideToast, 8000);
  }

  // ---------------------------------------------------------------------
  // Keyboard shortcuts
  // ---------------------------------------------------------------------

  function goToAdjacentChapter(direction) {
    if (!chapterSections.length) return;

    const marker = window.scrollY + 160;
    let index = 0;
    chapterSections.forEach((section, sectionIndex) => {
      if (section.getBoundingClientRect().top + window.scrollY <= marker) {
        index = sectionIndex;
      }
    });

    const targetIndex = Math.max(
      0,
      Math.min(chapterSections.length - 1, index + direction)
    );
    chapterSections[targetIndex].scrollIntoView({
      behavior: reducedMotion ? "auto" : "smooth",
      block: "start",
    });
  }

  document.addEventListener("keydown", (event) => {
    if (event.altKey || event.ctrlKey || event.metaKey) return;

    if (event.key === "Escape") {
      if (settingsOpen) {
        closeSettings();
      } else if (focusOpen) {
        closeFocus();
      } else {
        closeNav();
        hideToast();
      }
      return;
    }

    const tag = event.target && event.target.tagName;
    if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;

    const isSettingsKey = event.key === "s" || event.key === "S" || event.key === "?";

    if (settingsOpen) {
      if (event.key === "t" || event.key === "T") {
        toggleTheme();
      } else if (event.key === "+" || event.key === "=") {
        event.preventDefault();
        fontSize = setFontSize(fontSize + 1);
      } else if (event.key === "-" || event.key === "_") {
        event.preventDefault();
        fontSize = setFontSize(fontSize - 1);
      } else if (isSettingsKey) {
        closeSettings();
      }
      return;
    }

    if (focusOpen) {
      if (event.key === "ArrowLeft" || event.key === "h" || event.key === "H") {
        event.preventDefault();
        showFocusScene(currentSceneIndex - 1);
      } else if (
        event.key === "ArrowRight" ||
        event.key === "l" ||
        event.key === "L"
      ) {
        event.preventDefault();
        showFocusScene(currentSceneIndex + 1);
      } else if (event.key === "Home") {
        event.preventDefault();
        showFocusScene(0);
      } else if (event.key === "End") {
        event.preventDefault();
        showFocusScene(sceneItems.length - 1);
      } else if (event.key === "f" || event.key === "F") {
        focusFullscreen.click();
      } else if (event.key === "c" || event.key === "C") {
        event.preventDefault();
        setChromeHidden(!focusReader.classList.contains("chrome-hidden"));
      } else if (event.key === "t" || event.key === "T") {
        toggleTheme();
      } else if (isSettingsKey) {
        openSettings();
      } else if (event.key === "+" || event.key === "=") {
        event.preventDefault();
        fontSize = setFontSize(fontSize + 1);
      } else if (event.key === "-" || event.key === "_") {
        event.preventDefault();
        fontSize = setFontSize(fontSize - 1);
      }
      return;
    }

    if (event.key === "t" || event.key === "T") {
      toggleTheme();
    } else if (isSettingsKey) {
      openSettings();
    } else if (event.key === "+" || event.key === "=") {
      event.preventDefault();
      fontSize = setFontSize(fontSize + 1);
    } else if (event.key === "-" || event.key === "_") {
      event.preventDefault();
      fontSize = setFontSize(fontSize - 1);
    } else if (event.key === "[" || event.key === "]") {
      event.preventDefault();
      goToAdjacentChapter(event.key === "[" ? -1 : 1);
    } else if (event.key === "f" || event.key === "F") {
      openFocus();
    }
  });

  // ---------------------------------------------------------------------
  // Render and restore
  // ---------------------------------------------------------------------

  function restoreReadingPosition(volume) {
    const savedScroll =
      Number(storage.get(volumeStorageKey("scroll"))) ||
      (volume === 15 ? Number(storage.get("mt15:scroll")) || 0 : 0);
    const hasHash = Boolean(window.location.hash);

    if (hasHash) {
      const target = document.querySelector(window.location.hash);
      if (target) {
        window.requestAnimationFrame(() => {
          const targetTop =
            target.getBoundingClientRect().top + window.scrollY - 82;
          jumpTo(targetTop);
          updateScrollUi();
        });
      }
      return;
    }

    if (savedScroll > 240) {
      window.requestAnimationFrame(() => {
        jumpTo(savedScroll);
        updateScrollUi();
        showToast("Returned to where you left off.", "Start over", () => {
          window.scrollTo({ top: 0, behavior: reducedMotion ? "auto" : "smooth" });
        });
      });
    }
  }

  const storedVolume = Number(storage.get("mt15:last-volume"));
  const urlVolume = volumeFromUrl();
  const initialVolume =
    urlVolume !== null
      ? urlVolume
      : volumeOrder.includes(storedVolume)
        ? storedVolume
        : volumeOrder[0];

  reader.classList.add("is-loading");
  loadVolumeData(initialVolume)
    .then((volumeData) => {
      data = volumeData;
      activeVolume = initialVolume;
      storage.set("mt15:last-volume", String(initialVolume));
      reader.classList.remove("is-loading");
      renderCurrentVolume();
      restoreReadingPosition(initialVolume);
    })
    .catch(() => {
      reader.classList.remove("is-loading");
      reader.innerHTML =
        '<p class="load-error">The volume data could not be loaded. Make sure <code>data.js</code> and the <code>volumes</code> folder are next to <code>index.html</code>.</p>';
    });
})();
