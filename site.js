(() => {
  "use strict";
  const reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)",
  ).matches;
  // Content is visible by default. Only reveal below-fold projects when supported.
  if (!reduceMotion && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08 },
    );
    document.querySelectorAll(".reveal").forEach((el) => {
      if (el.getBoundingClientRect().top > window.innerHeight) {
        el.classList.add("reveal-ready");
        observer.observe(el);
      }
    });
  }
  const dialog = document.querySelector(".image-dialog");
  if (!dialog || typeof dialog.showModal !== "function") return;
  const image = dialog.querySelector("img");
  const caption = dialog.querySelector("p");
  let trigger = null;
  document.querySelectorAll("[data-zoom]").forEach((link) => {
    link.addEventListener("click", (event) => {
      // Preserve standard open-in-new-tab and no-JavaScript link behaviour.
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)
        return;
      event.preventDefault();
      trigger = link;
      image.src = link.href;
      image.alt = link.querySelector("img").alt;
      caption.textContent =
        link.closest("figure").querySelector("figcaption")?.textContent ||
        image.alt;
      dialog.showModal();
    });
  });
  dialog
    .querySelector(".dialog-close")
    .addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener("close", () => {
    if (trigger) trigger.focus({ preventScroll: true });
  });
})();
