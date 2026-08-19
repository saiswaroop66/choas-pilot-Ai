/* =========================================================
   CHAOSPILOT — LANDING PAGE JAVASCRIPT
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    initializeNavigation();
    initializeMobileMenu();
    initializeButtons();
    initializePricing();
    initializeScrollEffects();
    initializeRevealAnimations();

});


/* =========================================================
   NAVIGATION
   ========================================================= */

function initializeNavigation() {

    const navLinks =
        document.querySelectorAll(
            'a[href^="#"]'
        );


    navLinks.forEach(link => {

        link.addEventListener(
            "click",
            event => {

                const targetId =
                    link.getAttribute("href");


                if (
                    !targetId ||
                    targetId === "#"
                ) {
                    return;
                }


                const target =
                    document.querySelector(
                        targetId
                    );


                if (!target) return;


                event.preventDefault();


                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }
        );

    });

}


/* =========================================================
   MOBILE MENU
   ========================================================= */

function initializeMobileMenu() {

    const menuButton =
        document.querySelector(
            ".mobile-menu-button"
        );


    const mobileMenu =
        document.querySelector(
            ".mobile-menu"
        );


    if (!menuButton || !mobileMenu) {
        return;
    }


    menuButton.addEventListener(
        "click",
        () => {

            mobileMenu.classList.toggle(
                "open"
            );

            menuButton.classList.toggle(
                "active"
            );

        }
    );


    mobileMenu
        .querySelectorAll("a")
        .forEach(link => {

            link.addEventListener(
                "click",
                () => {

                    mobileMenu.classList.remove(
                        "open"
                    );

                    menuButton.classList.remove(
                        "active"
                    );

                }
            );

        });

}


/* =========================================================
   MAIN BUTTONS
   ========================================================= */

function initializeButtons() {

    const buttons =
        document.querySelectorAll(
            "a, button"
        );


    buttons.forEach(button => {

        const text =
            button.textContent
                .trim()
                .toLowerCase();


        /*
         * Get Started
         */

        if (
            text.includes(
                "get started"
            ) ||
            text.includes(
                "start monitoring"
            ) ||
            text.includes(
                "try chaospilot"
            )
        ) {

            button.addEventListener(
                "click",
                event => {

                    const href =
                        button.getAttribute(
                            "href"
                        );


                    if (
                        href &&
                        href !== "#"
                    ) {
                        return;
                    }


                    event.preventDefault();


                    window.location.href =
                        "login.html";

                }
            );

        }


        /*
         * Login
         */

        if (
            text === "login" ||
            text === "sign in"
        ) {

            button.addEventListener(
                "click",
                event => {

                    const href =
                        button.getAttribute(
                            "href"
                        );


                    if (
                        href &&
                        href !== "#"
                    ) {
                        return;
                    }


                    event.preventDefault();


                    window.location.href =
                        "login.html";

                }
            );

        }

    });

}


/* =========================================================
   PRICING / SUBSCRIPTION
   ========================================================= */

function initializePricing() {

    const pricingButtons =
        document.querySelectorAll(
            ".pricing-card button, \
             .pricing-button, \
             .subscription-button"
        );


    pricingButtons.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                const card =
                    button.closest(
                        ".pricing-card"
                    );


                let plan =
                    "selected plan";


                if (card) {

                    const title =
                        card.querySelector(
                            "h3, h2, .plan-name"
                        );


                    if (title) {
                        plan =
                            title.textContent
                                .trim();
                    }

                }


                showLandingToast(
                    `${plan} selected`,
                    "info"
                );


                setTimeout(() => {

                    window.location.href =
                        "login.html";

                }, 700);

            }
        );

    });

}


/* =========================================================
   NAVBAR SCROLL EFFECT
   ========================================================= */

function initializeScrollEffects() {

    const navbar =
        document.querySelector(
            "header, .navbar, .topbar"
        );


    if (!navbar) return;


    function updateNavbar() {

        if (window.scrollY > 40) {

            navbar.classList.add(
                "scrolled"
            );

        } else {

            navbar.classList.remove(
                "scrolled"
            );

        }

    }


    window.addEventListener(
        "scroll",
        updateNavbar
    );


    updateNavbar();

}


/* =========================================================
   REVEAL ANIMATIONS
   ========================================================= */

function initializeRevealAnimations() {

    const elements =
        document.querySelectorAll(
            ".feature-card, \
             .pricing-card, \
             .section-heading, \
             .hero-content, \
             .hero-visual, \
             .stat-card, \
             .solution-card"
        );


    if (!elements.length) {
        return;
    }


    elements.forEach(element => {

        element.classList.add(
            "reveal-element"
        );

    });


    const observer =
        new IntersectionObserver(
            entries => {

                entries.forEach(entry => {

                    if (
                        entry.isIntersecting
                    ) {

                        entry.target.classList.add(
                            "reveal-visible"
                        );

                        observer.unobserve(
                            entry.target
                        );

                    }

                });

            },
            {
                threshold: 0.12
            }
        );


    elements.forEach(element => {

        observer.observe(element);

    });

}


/* =========================================================
   LANDING PAGE TOAST
   ========================================================= */

function showLandingToast(
    message,
    type = "info"
) {

    const existing =
        document.querySelector(
            ".landing-toast"
        );


    if (existing) {
        existing.remove();
    }


    const toast =
        document.createElement(
            "div"
        );


    toast.className =
        `landing-toast ${type}`;


    toast.innerHTML = `

        <span class="toast-dot">
            ●
        </span>

        <span>
            ${escapeHTML(message)}
        </span>

    `;


    document.body.appendChild(
        toast
    );


    setTimeout(() => {

        toast.classList.add(
            "hide"
        );


        setTimeout(() => {

            toast.remove();

        }, 300);

    }, 2200);

}


/* =========================================================
   SAFE HTML
   ========================================================= */

function escapeHTML(value) {

    const element =
        document.createElement(
            "div"
        );


    element.textContent =
        value;


    return element.innerHTML;

}


/* =========================================================
   ACTIVE NAVIGATION
   ========================================================= */

window.addEventListener(
    "scroll",
    () => {

        const sections =
            document.querySelectorAll(
                "section[id]"
            );


        const links =
            document.querySelectorAll(
                'nav a[href^="#"]'
            );


        let currentSection = "";


        sections.forEach(section => {

            const sectionTop =
                section.offsetTop - 150;


            if (
                window.scrollY >=
                sectionTop
            ) {

                currentSection =
                    section.id;

            }

        });


        links.forEach(link => {

            link.classList.remove(
                "active"
            );


            const href =
                link.getAttribute(
                    "href"
                );


            if (
                href ===
                `#${currentSection}`
            ) {

                link.classList.add(
                    "active"
                );

            }

        });

    }
);


/* =========================================================
   CONSOLE INFORMATION
   ========================================================= */

console.log(
    "%cChaosPilot",
    "font-size:20px;font-weight:bold;"
);

console.log(
    "AI-powered software resilience engineering platform."
);

console.log(
    "Frontend initialized successfully."
);