(function () {
  var root = document.documentElement, key = "sdrviewer-manual-theme", saved = null;
  try { saved = localStorage.getItem(key); } catch (e) {}
  if (saved) root.setAttribute("data-theme", saved);
  document.addEventListener("DOMContentLoaded", function () {
    var t = document.getElementById("theme");
    if (t) t.addEventListener("click", function () {
      var dark = root.getAttribute("data-theme") ? root.getAttribute("data-theme") === "dark"
        : window.matchMedia("(prefers-color-scheme: dark)").matches;
      var next = dark ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem(key, next); } catch (e) {}
    });
    var m = document.getElementById("menu");
    if (m) m.addEventListener("click", function () { document.body.classList.toggle("open"); });
    var soon = document.body.getAttribute("data-soon") || "";
    document.querySelectorAll("nav.side a.soon").forEach(function (a) { a.setAttribute("data-soon", soon); });
    document.querySelectorAll("pre").forEach(function (pre) {
      var b = document.createElement("button"); var T = window.MANUAL || {copy: "Copy", copied: "Copied"};
      b.className = "copy"; b.textContent = T.copy;
      b.addEventListener("click", function () {
        var text = pre.querySelector("code").innerText;
        (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(function () {
          b.textContent = T.copied; setTimeout(function () { b.textContent = T.copy; }, 1400);
        }, function () { b.textContent = "⌘C"; });
      });
      pre.appendChild(b);
    });
  });
})();
