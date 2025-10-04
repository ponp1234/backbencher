// Footer year
document.addEventListener("DOMContentLoaded", () => {
  const yearEl = document.getElementById("y");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
});

// Mobile menu
const btn = document.getElementById("menuBtn");
const menu = document.getElementById("mobileMenu");
if (btn && menu) {
  btn.addEventListener("click", () => {
    const isOpen = menu.classList.toggle("show");
    btn.setAttribute("aria-expanded", String(isOpen));
  });
}

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
