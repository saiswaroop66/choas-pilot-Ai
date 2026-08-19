/* =========================================================
   CHAOSPILOT AUTHENTICATION
   Frontend Authentication Prototype
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "ChaosPilot Auth initialized"
        );


        setupLogin();

        setupPasswordToggle();

        setupDemoLogin();

        setupForgotPassword();

        setupRegister();


        /*
         * Protect dashboard
         */

        protectDashboard();

    }
);


/* =========================================================
   LOGIN
   ========================================================= */

function setupLogin() {

    const form =
        document.getElementById(
            "loginForm"
        );


    if (!form) {

        console.log(
            "Login form not found on this page."
        );

        return;

    }


    form.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();


            const email =
                document
                    .getElementById(
                        "loginEmail"
                    )
                    .value
                    .trim();


            const password =
                document
                    .getElementById(
                        "loginPassword"
                    )
                    .value
                    .trim();


            clearErrors();


            /* Validate email */

            if (!email) {

                showError(
                    "loginEmail",
                    "Email is required."
                );

                return;

            }


            if (!isValidEmail(email)) {

                showError(
                    "loginEmail",
                    "Enter a valid email address."
                );

                return;

            }


            /* Validate password */

            if (!password) {

                showError(
                    "loginPassword",
                    "Password is required."
                );

                return;

            }


            if (password.length < 6) {

                showError(
                    "loginPassword",
                    "Password must contain at least 6 characters."
                );

                return;

            }


            loginButtonLoading(true);


            /*
             * FRONTEND DEMO AUTH
             *
             * Backend authentication will
             * replace this later.
             */

            setTimeout(
                function () {

                    const user = {

                        email: email,

                        loggedIn: true,

                        loginTime:
                            new Date()
                                .toISOString()

                    };


                    localStorage.setItem(
                        "chaospilot_user",
                        JSON.stringify(user)
                    );


                    localStorage.setItem(
                        "chaospilot_logged_in",
                        "true"
                    );


                    showMessage(
                        "Login successful. Opening dashboard...",
                        "success"
                    );


                    /*
                     * IMPORTANT
                     *
                     * login.html and
                     * dashboard.html are
                     * in the same folder.
                     */

                    setTimeout(
                        function () {

                            window.location.replace(
                                "./dashboard.html"
                            );

                        },
                        700
                    );

                },
                900
            );

        }
    );

}


/* =========================================================
   LOGIN BUTTON
   ========================================================= */

function loginButtonLoading(
    loading
) {

    const button =
        document.getElementById(
            "loginButton"
        );


    if (!button) return;


    if (loading) {

        button.disabled = true;

        button.dataset.originalText =
            button.innerHTML;

        button.innerHTML = `

            <span>
                Authenticating...
            </span>

            <span class="button-spinner"></span>

        `;

    } else {

        button.disabled = false;

        button.innerHTML =
            button.dataset.originalText ||
            `
            <span>
                Sign in to ChaosPilot
            </span>

            <span>
                →
            </span>
            `;

    }

}


/* =========================================================
   PASSWORD TOGGLE
   ========================================================= */

function setupPasswordToggle() {

    const button =
        document.getElementById(
            "passwordToggle"
        );


    if (!button) return;


    button.addEventListener(
        "click",
        function () {

            const password =
                document.getElementById(
                    "loginPassword"
                );


            if (!password) return;


            if (
                password.type ===
                "password"
            ) {

                password.type =
                    "text";

                button.textContent =
                    "Hide";

            } else {

                password.type =
                    "password";

                button.textContent =
                    "Show";

            }

        }
    );

}


/* =========================================================
   DEMO LOGIN
   ========================================================= */

function setupDemoLogin() {

    const button =
        document.getElementById(
            "demoLogin"
        );


    if (!button) return;


    button.addEventListener(
        "click",
        function () {

            const email =
                document.getElementById(
                    "loginEmail"
                );


            const password =
                document.getElementById(
                    "loginPassword"
                );


            if (email) {

                email.value =
                    "demo@chaospilot.ai";

            }


            if (password) {

                password.value =
                    "chaospilot123";

            }


            showMessage(
                "Demo account loaded.",
                "info"
            );

        }
    );

}


/* =========================================================
   FORGOT PASSWORD
   ========================================================= */

function setupForgotPassword() {

    const link =
        document.getElementById(
            "forgotPassword"
        );


    if (!link) return;


    link.addEventListener(
        "click",
        function (event) {

            event.preventDefault();


            showMessage(
                "Password recovery will be available after backend authentication is connected.",
                "info"
            );

        }
    );

}


/* =========================================================
   REGISTER
   ========================================================= */

function setupRegister() {

    const link =
        document.getElementById(
            "registerLink"
        );


    if (!link) return;


    link.addEventListener(
        "click",
        function (event) {

            event.preventDefault();


            showMessage(
                "Registration will be connected to the backend in the next phase.",
                "info"
            );

        }
    );

}


/* =========================================================
   VALIDATE EMAIL
   ========================================================= */

function isValidEmail(
    email
) {

    const pattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


    return pattern.test(email);

}


/* =========================================================
   SHOW ERROR
   ========================================================= */

function showError(
    inputId,
    message
) {

    const input =
        document.getElementById(
            inputId
        );


    if (!input) return;


    input.classList.add(
        "input-error"
    );


    const parent =
        input.parentElement;


    let error =
        parent.querySelector(
            ".field-error"
        );


    if (!error) {

        error =
            document.createElement(
                "div"
            );

        error.className =
            "field-error";

        parent.appendChild(
            error
        );

    }


    error.textContent =
        message;


    input.focus();

}


/* =========================================================
   CLEAR ERRORS
   ========================================================= */

function clearErrors() {

    document
        .querySelectorAll(
            ".input-error"
        )
        .forEach(
            function (input) {

                input.classList.remove(
                    "input-error"
                );

            }
        );


    document
        .querySelectorAll(
            ".field-error"
        )
        .forEach(
            function (error) {

                error.remove();

            }
        );

}


/* =========================================================
   MESSAGE
   ========================================================= */

function showMessage(
    message,
    type = "info"
) {

    const old =
        document.querySelector(
            ".login-message"
        );


    if (old) {

        old.remove();

    }


    const box =
        document.createElement(
            "div"
        );


    box.className =
        `login-message ${type}`;


    let icon = "●";


    if (type === "success") {

        icon = "✓";

    }


    if (type === "error") {

        icon = "×";

    }


    if (type === "warning") {

        icon = "⚠";

    }


    box.innerHTML = `

        <div class="login-message-icon">

            ${icon}

        </div>

        <p>
            ${escapeHTML(message)}
        </p>

    `;


    document.body.appendChild(
        box
    );


    setTimeout(
        function () {

            box.classList.add(
                "hide"
            );


            setTimeout(
                function () {

                    box.remove();

                },
                300
            );

        },
        3000
    );

}


/* =========================================================
   PROTECT DASHBOARD
   ========================================================= */

function protectDashboard() {

    const currentPage =
        window.location.pathname
            .split("/")
            .pop()
            .toLowerCase();


    /*
     * Only protect dashboard.html
     */

    if (
        currentPage !==
        "dashboard.html"
    ) {

        return;

    }


    const loggedIn =
        localStorage.getItem(
            "chaospilot_logged_in"
        );


    if (
        loggedIn !==
        "true"
    ) {

        window.location.replace(
            "./login.html"
        );

    }

}


/* =========================================================
   LOGOUT
   ========================================================= */

function logoutChaosPilot() {

    localStorage.removeItem(
        "chaospilot_user"
    );


    localStorage.removeItem(
        "chaospilot_logged_in"
    );


    window.location.replace(
        "./login.html"
    );

}


/* =========================================================
   HTML ESCAPE
   ========================================================= */

function escapeHTML(
    value
) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        value;


    return div.innerHTML;

}


/* =========================================================
   GLOBAL LOGOUT
   ========================================================= */

window.logoutChaosPilot =
    logoutChaosPilot;