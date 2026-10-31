/* Speaker-aware chapter voiceover.
 *
 * Reads window.MUSOKU_AUDIO (chapter id -> track + block timings) and adds a
 * Listen button, a floating transport, block highlighting and click-to-seek.
 * The manifest is optional: if audio/manifest.js is missing the reader behaves
 * exactly as before, which keeps the public build free of narration tracks.
 */
(() => {
  "use strict";

  const CHAPTER_SELECTOR = ".chapter[data-chapter-id]";
  const STORAGE_PREFIX = "mt-audio:";

  let manifest = null;
  let audio = null;
  let active = null;
  let blocks = [];
  let currentIndex = -1;
  let follow = true;
  let saveTimer = 0;
  let pendingSeek = null;

  const ui = {};

  /* ---------------------------------------------------------------- helpers */

  function currentVolume() {
    const pressed = document.querySelector('.volume-nav__button[aria-pressed="true"]');
    return pressed ? pressed.dataset.volume : null;
  }

  function chapterAtViewport() {
    const chapters = [...document.querySelectorAll(CHAPTER_SELECTOR)];
    if (!chapters.length) return null;
    const anchor = 140;
    let found = chapters[0];
    for (const chapter of chapters) {
      if (chapter.getBoundingClientRect().top <= anchor) found = chapter;
      else break;
    }
    return found.dataset.chapterId;
  }

  function resolve(volume, chapterId) {
    if (!manifest) return null;
    const entry = manifest[`${volume}:${chapterId}`];
    if (!entry) return null;
    return { ...entry, volume, chapterId, key: `${volume}:${chapterId}` };
  }

  function blockElement(id) {
    return document.querySelector(`[data-block-id="${CSS.escape(id)}"]`);
  }

  function trackUrl(file) {
    try {
      return new URL(file, window.location.href).href;
    } catch {
      return file;
    }
  }

  function clock(seconds) {
    if (!Number.isFinite(seconds)) return "0:00";
    const total = Math.max(0, Math.floor(seconds));
    const minutes = Math.floor(total / 60);
    const rest = total % 60;
    if (minutes >= 60) {
      return `${Math.floor(minutes / 60)}:${String(minutes % 60).padStart(2, "0")}:${String(rest).padStart(2, "0")}`;
    }
    return `${minutes}:${String(rest).padStart(2, "0")}`;
  }

  function savedPosition(key) {
    try {
      const value = Number(localStorage.getItem(STORAGE_PREFIX + key));
      return Number.isFinite(value) ? value : 0;
    } catch {
      return 0;
    }
  }

  function savePosition() {
    if (!active || !audio) return;
    try {
      localStorage.setItem(STORAGE_PREFIX + active.key, String(audio.currentTime));
    } catch {
      /* file:// or private mode */
    }
  }

  /* -------------------------------------------------------------- transport */

  function ensureAudio() {
    if (audio) return audio;
    audio = document.createElement("audio");
    audio.preload = "metadata";
    audio.addEventListener("timeupdate", onTime);
    audio.addEventListener("play", () => {
      ui.bar.classList.add("is-playing");
      ui.play.textContent = "❚❚";
      ui.play.setAttribute("aria-label", "Pause");
      ui.toggle.setAttribute("aria-pressed", "true");
    });
    audio.addEventListener("pause", () => {
      ui.bar.classList.remove("is-playing");
      ui.play.textContent = "▶";
      ui.play.setAttribute("aria-label", "Play");
      ui.toggle.setAttribute("aria-pressed", "false");
      savePosition();
    });
    audio.addEventListener("loadedmetadata", () => {
      ui.duration.textContent = clock(audio.duration);
      ui.seek.max = String(Math.floor(audio.duration * 10));
      if (pendingSeek != null) {
        audio.currentTime = Math.min(pendingSeek, Math.max(0, audio.duration - 1));
        pendingSeek = null;
      }
    });
    document.body.appendChild(audio);
    return audio;
  }

  function bindBlocks(entry) {
    blocks = entry.blocks
      .map((block) => ({ ...block, el: blockElement(block.id) }))
      .filter((block) => block.el)
      .sort((a, b) => a.start - b.start);
  }

  function highlight(index) {
    if (index === currentIndex) return;
    if (currentIndex >= 0 && blocks[currentIndex]) {
      blocks[currentIndex].el.classList.remove("block--speaking");
    }
    currentIndex = index;
    const block = blocks[index];
    if (!block) return;
    block.el.classList.add("block--speaking");
    if (follow) {
      const rect = block.el.getBoundingClientRect();
      const bar = ui.bar.getBoundingClientRect();
      const top = 90;
      const bottom = window.innerHeight - (bar.height || 90) - 24;
      if (rect.top < top || rect.bottom > bottom) {
        block.el.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      }
    }
  }

  function onTime() {
    if (!audio || !blocks.length) return;
    const t = audio.currentTime;
    ui.elapsed.textContent = clock(t);
    if (document.activeElement !== ui.seek) {
      ui.seek.value = String(Math.floor(t * 10));
      ui.seek.style.setProperty("--p", `${(t / (audio.duration || 1)) * 100}%`);
    }
    let index = -1;
    for (let i = 0; i < blocks.length; i += 1) {
      if (t >= blocks[i].start && t < blocks[i].end + 0.01) {
        index = i;
        break;
      }
    }
    if (index === -1) {
      for (let i = blocks.length - 1; i >= 0; i -= 1) {
        if (t >= blocks[i].start) {
          index = i;
          break;
        }
      }
    }
    highlight(index);
    if (Date.now() - saveTimer > 4000) {
      saveTimer = Date.now();
      savePosition();
    }
  }

  function start(entry) {
    ensureAudio();
    if (active && active.key === entry.key) {
      audio.play();
      return;
    }
    active = entry;
    bindBlocks(entry);
    audio.src = trackUrl(entry.file);
    ui.bar.hidden = false;
    ui.chapter.textContent = entry.label || `Chapter ${entry.chapterId.replace(/\D/g, "")}`;
    ui.duration.textContent = clock(entry.duration);
    const resume = savedPosition(entry.key);
    const chapterStart = blocks.length ? blocks[0].start : 0;
    const chapterEnd = entry.duration || 0;
    pendingSeek =
      resume > chapterStart && resume < chapterEnd - 3 ? resume : seekTargetForViewport(chapterStart);
    ui.toggle.setAttribute("aria-pressed", "true");
    audio.play().catch(() => {
      /* the transport button is still there if the browser refuses */
    });
  }

  function seekTargetForViewport(fallback) {
    for (const block of blocks) {
      const rect = block.el.getBoundingClientRect();
      if (rect.bottom > 140) return Math.max(block.start, fallback);
    }
    return fallback;
  }

  function stop() {
    if (!audio) return;
    audio.pause();
    savePosition();
    if (currentIndex >= 0 && blocks[currentIndex]) {
      blocks[currentIndex].el.classList.remove("block--speaking");
    }
    currentIndex = -1;
    active = null;
    blocks = [];
    ui.bar.hidden = true;
    ui.toggle.setAttribute("aria-pressed", "false");
  }

  function seekTo(seconds) {
    if (!audio) return;
    audio.currentTime = Math.max(0, seconds);
    onTime();
  }

  /* ---------------------------------------------------------------- sharing */

  async function loadManifest() {
    if (window.MUSOKU_AUDIO) {
      manifest = window.MUSOKU_AUDIO;
      return true;
    }
    return new Promise((resolve) => {
      const script = document.createElement("script");
      script.src = "audio/manifest.js";
      script.onload = () => {
        manifest = window.MUSOKU_AUDIO || null;
        resolve(Boolean(manifest));
      };
      script.onerror = () => resolve(false);
      document.head.appendChild(script);
    });
  }

  /* --------------------------------------------------------------------- ui */

  function buildUi() {
    ui.toggle = document.createElement("button");
    ui.toggle.type = "button";
    ui.toggle.className = "icon-button audio-toggle";
    ui.toggle.id = "audioToggle";
    ui.toggle.title = "Listen to this chapter";
    ui.toggle.setAttribute("aria-label", "Listen to this chapter");
    ui.toggle.setAttribute("aria-pressed", "false");
    ui.toggle.innerHTML =
      '<svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M4 9.5v5h3.2L12 18.5v-13L7.2 9.5H4Z"/>' +
      '<path d="M15.5 8.5a5 5 0 0 1 0 7"/>' +
      '<path d="M18 6a8.5 8.5 0 0 1 0 12"/>' +
      "</svg>";

    const actions = document.querySelector(".topbar__actions");
    if (actions) actions.insertBefore(ui.toggle, actions.firstChild);

    ui.bar = document.createElement("div");
    ui.bar.className = "audio-bar";
    ui.bar.hidden = true;
    ui.bar.innerHTML = `
      <button type="button" class="audio-bar__play" aria-label="Play">▶</button>
      <div class="audio-bar__meta">
        <span class="audio-bar__chapter"></span>
        <span class="audio-bar__clock"><span class="audio-bar__elapsed">0:00</span> / <span class="audio-bar__duration">0:00</span></span>
      </div>
      <input class="audio-bar__seek" type="range" min="0" max="100" value="0" step="1" aria-label="Seek">
      <select class="audio-bar__speed" aria-label="Playback speed">
        <option value="0.8">0.8×</option>
        <option value="1" selected>1×</option>
        <option value="1.15">1.15×</option>
        <option value="1.3">1.3×</option>
        <option value="1.5">1.5×</option>
      </select>
      <button type="button" class="audio-bar__follow" aria-pressed="true" title="Follow the narration">Follow</button>
      <button type="button" class="audio-bar__close" aria-label="Close player">×</button>
    `;
    document.body.appendChild(ui.bar);

    ui.play = ui.bar.querySelector(".audio-bar__play");
    ui.chapter = ui.bar.querySelector(".audio-bar__chapter");
    ui.elapsed = ui.bar.querySelector(".audio-bar__elapsed");
    ui.duration = ui.bar.querySelector(".audio-bar__duration");
    ui.seek = ui.bar.querySelector(".audio-bar__seek");
    ui.speed = ui.bar.querySelector(".audio-bar__speed");
    ui.follow = ui.bar.querySelector(".audio-bar__follow");
    ui.close = ui.bar.querySelector(".audio-bar__close");

    ui.toggle.addEventListener("click", async () => {
      if (active) {
        stop();
        return;
      }
      const volume = currentVolume();
      const chapterId = chapterAtViewport();
      const entry = resolve(volume, chapterId);
      if (!entry) {
        document.dispatchEvent(
          new CustomEvent("mt-audio-missing", { detail: { volume, chapterId } })
        );
        return;
      }
      start(entry);
    });

    ui.play.addEventListener("click", () => {
      if (!audio) return;
      if (audio.paused) audio.play();
      else audio.pause();
    });

    ui.seek.addEventListener("input", () => {
      if (!audio) return;
      audio.currentTime = Number(ui.seek.value) / 10;
    });

    ui.speed.addEventListener("change", () => {
      if (!audio) return;
      audio.playbackRate = Number(ui.speed.value);
    });

    ui.follow.addEventListener("click", () => {
      follow = !follow;
      ui.follow.setAttribute("aria-pressed", String(follow));
      ui.follow.classList.toggle("is-off", !follow);
    });

    ui.close.addEventListener("click", stop);

    document.addEventListener("click", (event) => {
      if (!active || !audio) return;
      const block = event.target.closest("[data-block-id]");
      if (!block) return;
      if (window.getSelection && String(window.getSelection())) return;
      const entry = blocks.find((item) => item.id === block.dataset.blockId);
      if (!entry) return;
      seekTo(entry.start);
    });

    document.addEventListener("keydown", (event) => {
      if (!active || !audio) return;
      if (event.altKey || event.ctrlKey || event.metaKey) return;
      if (event.code !== "Space") return;
      const tag = event.target && event.target.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || tag === "BUTTON") return;
      event.preventDefault();
      if (audio.paused) audio.play();
      else audio.pause();
    });

    window.addEventListener("beforeunload", savePosition);
  }

  async function init() {
    const available = await loadManifest();
    if (!available) return;
    buildUi();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
