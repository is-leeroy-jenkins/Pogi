/*
 * ==========================================================================================
 *  Pogi Documentation JavaScript
 *  File: docs/assets/js/pogi.js
 *
 *  Purpose:
 *      Provides lightweight progressive enhancements for the Pogi MkDocs site.
 * ==========================================================================================
 */

(function () {
    "use strict";

    function addScrollTopButton() {
        if (document.getElementById("pogi-scroll-top")) {
            return;
        }

        const button = document.createElement("button");
        button.id = "pogi-scroll-top";
        button.type = "button";
        button.textContent = "↑";
        button.setAttribute("aria-label", "Scroll to top");

        button.style.position = "fixed";
        button.style.right = "1rem";
        button.style.bottom = "1rem";
        button.style.display = "none";
        button.style.zIndex = "1000";
        button.style.borderRadius = "999px";
        button.style.padding = "0.55rem 0.8rem";
        button.style.border = "1px solid #4DA3FF";
        button.style.background = "#024FA3";
        button.style.color = "#FFFFFF";
        button.style.cursor = "pointer";

        button.addEventListener("click", function () {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });

        document.body.appendChild(button);

        window.addEventListener("scroll", function () {
            button.style.display = window.scrollY > 400 ? "block" : "none";
        }, { passive: true });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", addScrollTopButton);
    } else {
        addScrollTopButton();
    }
})();
