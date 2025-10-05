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

// Auth modal logic
    const backdrop = document.getElementById("authBackdrop");
    const modal = document.getElementById("authModal");
    const openSignup = document.getElementById("openSignup");
    const openLogin = document.getElementById("openLogin");
    const footerLogin = document.getElementById("footerLogin");
    const footerJoin = document.getElementById("footerJoin");
    const mLogin = document.getElementById("mLogin");
    const mJoin = document.getElementById("mJoin");
    const closeAuth = document.getElementById("closeAuth");
    const authTitle = document.getElementById("authTitle");
    const googleText = document.getElementById("googleText");
    const fullNameGroup = document.getElementById("fullNameGroup");
    const submitBtn = document.getElementById("primarySubmit");
    const switchText = document.getElementById("switchText");
    const switchLink = document.getElementById("switchLink");

    let mode = "signup"; // or "login"

    function setMode(m){
      mode = m;
      authTitle.textContent = m === "signup" ? "Sign up now. It is free" : "Welcome back";
      googleText.textContent = m === "signup" ? "Sign up with Google" : "Continue with Google";
      fullNameGroup.style.display = m === "signup" ? "block" : "none";
      submitBtn.textContent = m === "signup" ? "Sign up" : "Log in";
      switchText.textContent = m === "signup" ? "Already have an account" : "New to Backbench AI";
      switchLink.textContent = m === "signup" ? "Log in" : "Create an account";
      const reg = document.getElementById("registerLink");
      if (reg) reg.style.display = m === "login" ? "block" : "none";
    }

    function openAuth(m){
      setMode(m);
      backdrop.removeAttribute("hidden");
      modal.removeAttribute("hidden");
      document.body.style.overflow = "hidden";
      closeAuth.focus();
    }
    function hideAuth(){
      backdrop.setAttribute("hidden", "");
      modal.setAttribute("hidden", "");
      document.body.style.overflow = "";
    }

    const openers = [
      [openSignup, "signup"], [openLogin, "login"],
      [footerLogin, "login"], [footerJoin, "signup"],
      [mLogin, "login"], [mJoin, "signup"],
      [document.getElementById("ctaJoin"), "signup"]
    ];
    openers.forEach(([el, m]) => { if (el) el.addEventListener("click", e => { e.preventDefault(); openAuth(m); }); });

    closeAuth.addEventListener("click", hideAuth);
    backdrop.addEventListener("click", hideAuth);
    window.addEventListener("keydown", e => { if(e.key === "Escape") hideAuth(); });

    document.getElementById("togglePw").addEventListener("click", () => {
      const pw = document.getElementById("password");
      pw.type = pw.type === "password" ? "text" : "password";
    });

    document.getElementById("authForm").addEventListener("submit", e => {
      e.preventDefault();
      // Hook up your auth here
      submitBtn.disabled = true;
      setTimeout(() => { submitBtn.disabled = false; hideAuth(); }, 700);
    });

    document.getElementById("switchAnchor").addEventListener("click", e => {
      e.preventDefault();
      setMode(mode === "signup" ? "login" : "signup");
    });
