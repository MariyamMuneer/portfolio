(() => {
  "use strict";
  const motionPreference = matchMedia("(prefers-reduced-motion: reduce)");
  const running = new Set();
  const waiting = new Set();
  const canAnimate = typeof Element.prototype.animate === "function";
  document.documentElement.classList.add("js-ready");

  function motion(el, frames, options = {}) {
    if (!el || motionPreference.matches || !canAnimate) return null;
    el.classList.add("motion-ready");
    const animation = el.animate(frames, {
      duration: 750,
      easing: "cubic-bezier(.22,1,.36,1)",
      fill: "backwards",
      ...options,
    });
    running.add(animation);
    animation.finished
      .then(() => {
        running.delete(animation);
        el.classList.remove("motion-ready");
      })
      .catch(() => {
        running.delete(animation);
        el.classList.remove("motion-ready");
      });
    return animation;
  }

  // Short, overlapping entrances: no loader and no delay before navigation works.
  function enterPage() {
    if (motionPreference.matches || !canAnimate) return;
    const greeting = document.querySelector('[data-hero="greeting"]');
    if (greeting) {
      motion(
        greeting,
        [
          { opacity: 0, transform: "translateY(16px)" },
          { opacity: 1, transform: "translateY(0)" },
        ],
        { duration: 600 },
      );
      document.querySelectorAll('[data-hero="line"]').forEach((line, index) => {
        motion(
          line,
          [
            { opacity: 0, transform: "translateY(90%) rotate(2deg)" },
            { opacity: 1, transform: "translateY(0) rotate(0)" },
          ],
          { delay: 110 + index * 140, duration: 950 },
        );
      });
      motion(
        document.querySelector('[data-hero="portrait"]'),
        [
          {
            opacity: 0,
            transform: "translateY(35px) rotate(-4deg) scale(.96)",
          },
          { opacity: 1, transform: "translateY(0) rotate(0) scale(1)" },
        ],
        { delay: 210, duration: 1100 },
      );
      ["summary", "actions", "rule"].forEach((name, index) => {
        motion(
          document.querySelector(`[data-hero="${name}"]`),
          [
            { opacity: 0, transform: "translateY(15px)" },
            { opacity: 1, transform: "translateY(0)" },
          ],
          { delay: 390 + index * 100, duration: 650 },
        );
      });
    } else {
      document
        .querySelectorAll(
          ".case-intro > .eyebrow, .case-intro h1, .case-deck, .facts, .case-cover",
        )
        .forEach((el, index) => {
          motion(
            el,
            [
              { opacity: 0, transform: "translateY(24px)" },
              { opacity: 1, transform: "translateY(0)" },
            ],
            { delay: index * 90, duration: 800 },
          );
        });
    }
  }
  enterPage();

  // Observe individual compositions, rather than fading an entire long section.
  let observer;
  if (
    !motionPreference.matches &&
    canAnimate &&
    "IntersectionObserver" in window
  ) {
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          el.style.removeProperty("opacity");
          waiting.delete(el);
          motion(
            el,
            [
              { opacity: 0, transform: "translateY(36px) scale(.985)" },
              { opacity: 1, transform: "translateY(0) scale(1)" },
            ],
            { duration: el.matches(".creative-preview") ? 1000 : 750 },
          );
          el.dataset.revealed = "true";
          observer.unobserve(el);
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -25px 0px" },
    );
    document
      .querySelectorAll(
        "[data-reveal], .case-page .image-grid figure, .case-page .section-title, .next-project",
      )
      .forEach((el) => {
        if (el.getBoundingClientRect().top > innerHeight - 25) {
          el.style.opacity = "0";
          waiting.add(el);
          observer.observe(el);
        }
      });
  }

  // A small, finite cue. It stops once the visitor starts exploring.
  const cue = document.querySelector(".scroll-cue-arrow");
  const cueMotion = motion(
    cue,
    [
      { transform: "translateY(0)" },
      { transform: "translateY(5px)", offset: 0.5 },
      { transform: "translateY(0)" },
    ],
    { duration: 1800, delay: 1200, iterations: 4, easing: "ease-in-out" },
  );
  function stopScrollCue() {
    if (scrollY > 80) {
      cueMotion?.cancel();
      removeEventListener("scroll", stopScrollCue);
    }
  }
  addEventListener("scroll", stopScrollCue, { passive: true });

  // Native dialog provides focus containment and Escape handling on mobile.
  const menu = document.querySelector(".mobile-menu");
  const toggle = document.querySelector(".menu-toggle");
  let closingMenu = false;
  function closeMenu(animate = true) {
    if (!menu?.open || closingMenu) return;
    closingMenu = true;
    const finish = () => {
      menu.close();
      closingMenu = false;
    };
    const animation = animate
      ? motion(
          menu,
          [
            { opacity: 1, transform: "translateY(0)" },
            { opacity: 0, transform: "translateY(-12px)" },
          ],
          { duration: 160, fill: "forwards" },
        )
      : null;
    if (animation)
      animation.finished
        .then(() => {
          finish();
          animation.cancel();
        })
        .catch(finish);
    else finish();
  }
  if (menu && toggle && typeof menu.showModal === "function") {
    toggle.addEventListener("click", () => {
      menu.showModal();
      toggle.setAttribute("aria-expanded", "true");
      motion(
        menu,
        [
          { opacity: 0, transform: "translateY(-20px) scale(.98)" },
          { opacity: 1, transform: "translateY(0) scale(1)" },
        ],
        { duration: 420 },
      );
      menu.querySelectorAll("nav a").forEach((el, index) =>
        motion(
          el,
          [
            { opacity: 0, transform: "translateY(14px)" },
            { opacity: 1, transform: "translateY(0)" },
          ],
          { delay: 80 + index * 55, duration: 450 },
        ),
      );
    });
    // Keep Tab on the menu controls, including at the first/last boundary.
    menu.addEventListener("keydown", (event) => {
      if (event.key !== "Tab") return;
      const controls = [...menu.querySelectorAll("button, a[href]")];
      const first = controls[0];
      const last = controls[controls.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
    menu
      .querySelector(".menu-close")
      .addEventListener("click", () => closeMenu());
    menu.addEventListener("click", (event) => {
      if (event.target === menu) closeMenu();
    });
    menu.addEventListener("close", () => {
      toggle.setAttribute("aria-expanded", "false");
    });
    menu
      .querySelectorAll("nav a")
      .forEach((link) =>
        link.addEventListener("click", () => closeMenu(false)),
      );
    matchMedia("(min-width: 701px)").addEventListener("change", (event) => {
      if (event.matches) closeMenu(false);
    });
  } else {
    // Older browsers keep the regular navigation instead of exposing a dead menu.
    document.documentElement.classList.remove("js-ready");
  }

  // A brief response when following a case study; modified clicks remain native.
  document
    .querySelectorAll('.creative-work a[href$=".html"], .next-project a')
    .forEach((link) => {
      link.addEventListener("click", (event) => {
        if (
          motionPreference.matches ||
          !canAnimate ||
          event.defaultPrevented ||
          event.button !== 0 ||
          event.metaKey ||
          event.ctrlKey ||
          event.shiftKey ||
          event.altKey
        )
          return;
        event.preventDefault();
        const main = document.querySelector("main");
        const animation = motion(
          main,
          [
            { opacity: 1, transform: "translateY(0)" },
            { opacity: 0.25, transform: "translateY(-6px)" },
          ],
          { duration: 160 },
        );
        if (animation)
          animation.finished
            .then(() => location.assign(link.href))
            .catch(() => location.assign(link.href));
        else location.assign(link.href);
      });
    });

  // Restrained desktop-only surface response, scheduled once per animation frame.
  const finePointer = matchMedia("(hover: hover) and (pointer: fine)");
  document.querySelectorAll(".creative-preview").forEach((card) => {
    let frame = null;
    let bounds = null;
    let point = null;
    const reset = () => {
      if (frame) cancelAnimationFrame(frame);
      frame = null;
      bounds = null;
      point = null;
      card.style.removeProperty("--tilt-x");
      card.style.removeProperty("--tilt-y");
    };
    card.addEventListener("pointerenter", () => {
      bounds = card.getBoundingClientRect();
    });
    card.addEventListener("pointermove", (event) => {
      if (
        !finePointer.matches ||
        motionPreference.matches ||
        event.pointerType === "touch"
      )
        return;
      bounds ||= card.getBoundingClientRect();
      point = { x: event.clientX, y: event.clientY };
      if (frame) return;
      frame = requestAnimationFrame(() => {
        const x = Math.max(
          -0.5,
          Math.min(0.5, (point.x - bounds.left) / bounds.width - 0.5),
        );
        const y = Math.max(
          -0.5,
          Math.min(0.5, (point.y - bounds.top) / bounds.height - 0.5),
        );
        card.style.setProperty("--tilt-x", `${-y * 2}deg`);
        card.style.setProperty("--tilt-y", `${x * 2}deg`);
        frame = null;
      });
    });
    card.addEventListener("pointerleave", reset);
    card.addEventListener("blur", reset);
    motionPreference.addEventListener("change", reset);
    finePointer.addEventListener("change", reset);
  });

  // A small reading-position cue; never captures scrolling or keyboard focus.
  const progress = document.createElement("div");
  progress.className = "reading-progress";
  progress.setAttribute("aria-hidden", "true");
  document.body.prepend(progress);
  let progressFrame = null;
  function updatePosition() {
    progressFrame = null;
    const range = document.documentElement.scrollHeight - innerHeight;
    const value = range > 0 ? Math.max(0, Math.min(1, scrollY / range)) : 0;
    progress.style.transform = `scaleX(${value})`;
  }
  addEventListener(
    "scroll",
    () => {
      if (!progressFrame) progressFrame = requestAnimationFrame(updatePosition);
    },
    { passive: true },
  );
  addEventListener("resize", updatePosition);
  updatePosition();

  // Keep Work/About navigation oriented to the section currently in view.
  if ("IntersectionObserver" in window && document.querySelector(".home")) {
    const sections = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          document
            .querySelectorAll(".desktop-nav a, .mobile-menu nav a")
            .forEach((link) => {
              if (link.hash === `#${entry.target.id}`)
                link.setAttribute("aria-current", "location");
              else link.removeAttribute("aria-current");
            });
        });
      },
      { rootMargin: "-15% 0px -65% 0px" },
    );
    document
      .querySelectorAll(".creative-hero, #work, #about, #contact")
      .forEach((el) => sections.observe(el));
  }

  // A useful contact action, with visible and screen-reader feedback.
  document.querySelectorAll("[data-copy-email]").forEach((button) => {
    if (!navigator.clipboard?.writeText) return;
    button.hidden = false;
    const status = button.parentElement.querySelector(".copy-status");
    let resetTimer;
    button.addEventListener("click", async () => {
      clearTimeout(resetTimer);
      try {
        await navigator.clipboard.writeText(button.dataset.copyEmail);
        status.textContent = "Email copied";
        motion(
          button,
          [{ transform: "scale(.95)" }, { transform: "scale(1)" }],
          { duration: 280 },
        );
      } catch {
        status.textContent = "Use the email link to get in touch.";
      }
      resetTimer = setTimeout(() => {
        status.textContent = "";
      }, 3500);
    });
  });

  // Research images retain direct links when scripting is unavailable.
  const imageDialog = document.querySelector(".image-dialog");
  if (imageDialog && typeof imageDialog.showModal === "function") {
    const image = imageDialog.querySelector("img");
    const caption = imageDialog.querySelector("p");
    let trigger = null;
    document.querySelectorAll("[data-zoom]").forEach((link) =>
      link.addEventListener("click", (event) => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)
          return;
        event.preventDefault();
        trigger = link;
        image.src = link.href;
        image.alt = link.querySelector("img").alt;
        caption.textContent =
          link.closest("figure").querySelector("figcaption")?.textContent ||
          image.alt;
        imageDialog.showModal();
        motion(
          imageDialog,
          [
            { opacity: 0, transform: "translateY(15px) scale(.98)" },
            { opacity: 1, transform: "translateY(0) scale(1)" },
          ],
          { duration: 350 },
        );
      }),
    );
    imageDialog
      .querySelector(".dialog-close")
      .addEventListener("click", () => imageDialog.close());
    imageDialog.addEventListener("click", (event) => {
      if (event.target === imageDialog) imageDialog.close();
    });
    imageDialog.addEventListener("close", () =>
      trigger?.focus({ preventScroll: true }),
    );
  }

  motionPreference.addEventListener("change", (event) => {
    if (event.matches) {
      running.forEach((animation) => animation.cancel());
      waiting.forEach((el) => el.style.removeProperty("opacity"));
      waiting.clear();
      observer?.disconnect();
    }
  });
  addEventListener("pageshow", (event) => {
    if (event.persisted) {
      running.forEach((animation) => animation.cancel());
      waiting.forEach((el) => el.style.removeProperty("opacity"));
      waiting.clear();
    }
  });
})();
