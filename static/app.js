// Footer year
document.addEventListener("DOMContentLoaded", () => {
  const y = document.getElementById("y");
  if (y) y.textContent = new Date().getFullYear();
});

// Mobile menu with body scroll lock + resize close
const btn = document.getElementById("menuBtn");
const menu = document.getElementById("mobileMenu");
if (btn && menu) {
  btn.addEventListener("click", () => {
    const isOpen = menu.classList.toggle("show");
    btn.setAttribute("aria-expanded", String(isOpen));
    document.body.style.overflow = isOpen ? "hidden" : "";
  });
  window.addEventListener("resize", () => {
    if (window.innerWidth > 900 && menu.classList.contains("show")) {
      menu.classList.remove("show");
      btn.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    }
  });
}

/* (keep your existing courses dropdown + auth modal code as-is) */

// Courses dropdown
const coursesBtn = document.getElementById("coursesBtn");
const coursesMenu = document.getElementById("coursesMenu");
let coursesOpen = false;
function toggleCourses(open) {
  coursesOpen = open;
  if (!coursesBtn || !coursesMenu) return;
  coursesMenu.classList.toggle("show", open);
  coursesBtn.setAttribute("aria-expanded", String(open));
}
if (coursesBtn) {
  coursesBtn.addEventListener("click", (e) => { e.preventDefault(); toggleCourses(!coursesOpen); });
  coursesBtn.addEventListener("mouseenter", () => { if (window.innerWidth > 900) toggleCourses(true); });
}
if (coursesMenu) {
  coursesMenu.addEventListener("mouseleave", () => { if (window.innerWidth > 900) toggleCourses(false); });
}
document.addEventListener("click", (e) => {
  if (!coursesOpen) return;
  if (!coursesMenu.contains(e.target) && !coursesBtn.contains(e.target)) toggleCourses(false);
});
