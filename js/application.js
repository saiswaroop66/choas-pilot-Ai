/* =========================================================
   CHAOSPILOT
   APPLICATION ONBOARDING JS
   ========================================================= */


document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeApplicationPage();

    }
);


/* =========================================================
   INITIALIZE
   ========================================================= */

function initializeApplicationPage() {

    setupNavigation();

    setupBackButton();

    setupCancelButton();

    setupConnectButton();

    setupLogout();

    loadExistingApplication();

}


/* =========================================================
   NAVIGATION
   ========================================================= */

function setupNavigation() {

    const links =
        document.querySelectorAll(
            ".nav-item"
        );


    links.forEach(link => {

        link.addEventListener(
            "click",
            function () {

                links.forEach(item => {

                    item.classList.remove(
                        "active"
                    );

                });


                this.classList.add(
                    "active"
                );

            }
        );

    });

}


/* =========================================================
   BACK BUTTON
   ========================================================= */

function setupBackButton() {

    const button =
        document.getElementById(
            "backButton"
        );


    if (!button)
        return;


    button.addEventListener(
        "click",
        () => {

            window.location.href =
                "./dashboard.html";

        }
    );

}


/* =========================================================
   CANCEL
   ========================================================= */

function setupCancelButton() {

    const button =
        document.getElementById(
            "cancelButton"
        );


    if (!button)
        return;


    button.addEventListener(
        "click",
        () => {

            window.location.href =
                "./dashboard.html";

        }
    );

}


/* =========================================================
   CONNECT APPLICATION
   ========================================================= */

function setupConnectButton() {

    const button =
        document.getElementById(
            "connectButton"
        );


    if (!button)
        return;


    button.addEventListener(
        "click",
        connectApplication
    );

}


/* =========================================================
   CONNECT
   ========================================================= */

function connectApplication() {

    const name =
        document
            .getElementById(
                "applicationName"
            )
            .value
            .trim();


    const url =
        document
            .getElementById(
                "applicationUrl"
            )
            .value
            .trim();


    const environment =
        document
            .getElementById(
                "environment"
            )
            .value;


    const type =
        document
            .getElementById(
                "applicationType"
            )
            .value;


    const description =
        document
            .getElementById(
                "description"
            )
            .value
            .trim();


    const technologies =
        getSelectedTechnologies();


    /* =====================================================
       VALIDATION
       ===================================================== */

    if (!name) {

        showMessage(
            "Please enter your application name.",
            "error"
        );

        focusElement(
            "applicationName"
        );

        return;

    }


    if (!url) {

        showMessage(
            "Please enter your application URL.",
            "error"
        );

        focusElement(
            "applicationUrl"
        );

        return;

    }


    if (!isValidURL(url)) {

        showMessage(
            "Please enter a valid application URL.",
            "error"
        );

        focusElement(
            "applicationUrl"
        );

        return;

    }


    if (!environment) {

        showMessage(
            "Please select an environment.",
            "error"
        );

        return;

    }


    if (!type) {

        showMessage(
            "Please select your application type.",
            "error"
        );

        return;

    }


    if (technologies.length === 0) {

        showMessage(
            "Select at least one technology.",
            "error"
        );

        return;

    }


    /* =====================================================
       APPLICATION OBJECT
       ===================================================== */

    const application = {

        id:
            generateApplicationId(),

        name:
            name,

        url:
            url,

        environment:
            environment,

        type:
            type,

        technologies:
            technologies,

        description:
            description,

        status:
            "connected",

        createdAt:
            new Date().toISOString()

    };


    /* =====================================================
       TEMPORARY STORAGE
       ===================================================== */

    localStorage.setItem(
        "chaospilot_application",
        JSON.stringify(application)
    );


    /* =====================================================
       BUTTON STATE
       ===================================================== */

    const button =
        document.getElementById(
            "connectButton"
        );


    const originalHTML =
        button.innerHTML;


    button.disabled = true;

    button.innerHTML =
        "Preparing analysis...";


    /* =====================================================
       TEMPORARY SIMULATION
       ===================================================== */

    setTimeout(() => {

        button.disabled = false;

        button.innerHTML =
            originalHTML;


        showSuccessScreen(
            application
        );

    }, 1800);

}


/* =========================================================
   SELECT TECHNOLOGIES
   ========================================================= */

function getSelectedTechnologies() {

    const checkboxes =
        document.querySelectorAll(
            ".technology input:checked"
        );


    return Array.from(
        checkboxes
    ).map(
        checkbox =>
            checkbox.value
    );

}


/* =========================================================
   VALIDATE URL
   ========================================================= */

function isValidURL(
    value
) {

    try {

        const url =
            new URL(value);


        return (
            url.protocol === "http:" ||
            url.protocol === "https:"
        );

    }

    catch {

        return false;

    }

}


/* =========================================================
   APPLICATION ID
   ========================================================= */

function generateApplicationId() {

    return (
        "app_" +
        Date.now() +
        "_" +
        Math.random()
            .toString(36)
            .substring(2, 8)
    );

}


/* =========================================================
   SUCCESS SCREEN
   ========================================================= */

function showSuccessScreen(
    application
) {

    const container =
        document.querySelector(
            ".onboarding-grid"
        );


    if (!container)
        return;


    container.innerHTML = `

        <div class="success-card">

            <div class="success-icon">
                ✓
            </div>


            <span class="success-eyebrow">
                APPLICATION CONNECTED
            </span>


            <h2>
                ${escapeHTML(application.name)}
                is ready for analysis
            </h2>


            <p>
                ChaosPilot has received your application
                information. The next step is to understand
                its architecture and service dependencies.
            </p>


            <div class="analysis-preview">

                <div>

                    <span>
                        APPLICATION
                    </span>

                    <strong>
                        ${escapeHTML(application.name)}
                    </strong>

                </div>


                <div>

                    <span>
                        ENVIRONMENT
                    </span>

                    <strong>
                        ${escapeHTML(
                            application.environment
                        )}
                    </strong>

                </div>


                <div>

                    <span>
                        TECHNOLOGIES
                    </span>

                    <strong>
                        ${application.technologies.length}
                    </strong>

                </div>

            </div>


            <div class="success-actions">

                <button
                    class="secondary-success-button"
                    id="backDashboard"
                >
                    Back to Dashboard
                </button>


                <button
                    class="primary-success-button"
                    id="startAnalysis"
                >
                    Start Architecture Analysis
                    →
                </button>

            </div>

        </div>

    `;


    addSuccessStyles();


    document
        .getElementById(
            "backDashboard"
        )
        .addEventListener(
            "click",
            () => {

                window.location.href =
                    "./dashboard.html";

            }
        );


    document
        .getElementById(
            "startAnalysis"
        )
        .addEventListener(
            "click",
            () => {

                startArchitectureAnalysis(
                    application
                );

            }
        );

}


/* =========================================================
   START ARCHITECTURE ANALYSIS
   ========================================================= */

function startArchitectureAnalysis(
    application
) {

    const button =
        document.getElementById(
            "startAnalysis"
        );


    button.disabled = true;

    button.innerHTML =
        "Preparing architecture analysis...";


    /*
     * FUTURE BACKEND CONNECTION
     *
     * Later this will become:
     *
     * fetch("/api/applications/analyze", {
     *     method: "POST",
     *     headers: {
     *         "Content-Type":
     *             "application/json"
     *     },
     *     body: JSON.stringify(application)
     * })
     */


    setTimeout(() => {

        localStorage.setItem(
            "chaospilot_analysis_status",
            "ready"
        );


        window.location.href =
            "./dashboard.html";

    }, 1800);

}


/* =========================================================
   LOAD EXISTING APPLICATION
   ========================================================= */

function loadExistingApplication() {

    const stored =
        localStorage.getItem(
            "chaospilot_application"
        );


    if (!stored)
        return;


    try {

        const application =
            JSON.parse(stored);


        const name =
            document.getElementById(
                "applicationName"
            );


        const url =
            document.getElementById(
                "applicationUrl"
            );


        if (name)
            name.value =
                application.name || "";


        if (url)
            url.value =
                application.url || "";


    }

    catch {

        console.log(
            "No saved application found."
        );

    }

}


/* =========================================================
   LOGOUT
   ========================================================= */

function setupLogout() {

    const button =
        document.getElementById(
            "logoutButton"
        );


    if (!button)
        return;


    button.addEventListener(
        "click",
        () => {

            localStorage.removeItem(
                "chaospilot_user"
            );


            localStorage.removeItem(
                "chaospilot_logged_in"
            );


            window.location.href =
                "./login.html";

        }
    );

}


/* =========================================================
   MESSAGE
   ========================================================= */

function showMessage(
    message,
    type = "error"
) {

    const existing =
        document.querySelector(
            ".application-message"
        );


    if (existing)
        existing.remove();


    const messageBox =
        document.createElement(
            "div"
        );


    messageBox.className =
        `application-message ${type}`;


    messageBox.innerHTML = `

        <span>
            ${type === "error" ? "!" : "✓"}
        </span>

        <p>
            ${escapeHTML(message)}
        </p>

    `;


    document.body.appendChild(
        messageBox
    );


    setTimeout(
        () => {

            messageBox.remove();

        },
        3000
    );

}


/* =========================================================
   FOCUS
   ========================================================= */

function focusElement(
    id
) {

    const element =
        document.getElementById(
            id
        );


    if (!element)
        return;


    element.focus();


    element.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

}


/* =========================================================
   ESCAPE HTML
   ========================================================= */

function escapeHTML(
    value
) {

    const element =
        document.createElement(
            "div"
        );


    element.textContent =
        value;


    return element.innerHTML;

}


/* =========================================================
   SUCCESS SCREEN STYLES
   ========================================================= */

function addSuccessStyles() {

    if (
        document.getElementById(
            "successStyles"
        )
    )
        return;


    const style =
        document.createElement(
            "style"
        );


    style.id =
        "successStyles";


    style.textContent = `

        .success-card {

            grid-column:
                1 / -1;

            min-height:
                500px;

            padding:
                55px;

            display:
                flex;

            flex-direction:
                column;

            align-items:
                center;

            justify-content:
                center;

            text-align:
                center;

            border:
                1px solid #273142;

            border-radius:
                14px;

            background:
                linear-gradient(
                    145deg,
                    #121a25,
                    #0f151e
                );

        }


        .success-icon {

            width:
                65px;

            height:
                65px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            border-radius:
                50%;

            background:
                #14291f;

            border:
                1px solid #2d6a47;

            color:
                #4ade80;

            font-size:
                28px;

            font-weight:
                900;

            box-shadow:
                0 0 35px
                rgba(74,222,128,.08);

        }


        .success-eyebrow {

            margin-top:
                25px;

            color:
                #4ade80;

            font-size:
                9px;

            font-weight:
                900;

            letter-spacing:
                1.3px;

        }


        .success-card h2 {

            max-width:
                700px;

            margin-top:
                9px;

            color:
                #ffffff;

            font-size:
                30px;

            letter-spacing:
                -.7px;

        }


        .success-card > p {

            max-width:
                650px;

            margin-top:
                12px;

            color:
                #7d899b;

            font-size:
                13px;

            line-height:
                1.7;

        }


        .analysis-preview {

            width:
                min(650px, 100%);

            margin-top:
                30px;

            padding:
                18px;

            display:
                grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap:
                10px;

            border:
                1px solid #273142;

            border-radius:
                10px;

            background:
                #0b1018;

        }


        .analysis-preview div {

            padding:
                10px;

            border-right:
                1px solid #242d3b;

        }


        .analysis-preview div:last-child {

            border-right:
                none;

        }


        .analysis-preview span {

            display:
                block;

            color:
                #5f6b7d;

            font-size:
                8px;

            font-weight:
                900;

            letter-spacing:
                .8px;

        }


        .analysis-preview strong {

            display:
                block;

            margin-top:
                6px;

            color:
                #dce1e8;

            font-size:
                12px;

        }


        .success-actions {

            margin-top:
                28px;

            display:
                flex;

            gap:
                10px;

        }


        .secondary-success-button,
        .primary-success-button {

            height:
                43px;

            padding:
                0 17px;

            border-radius:
                8px;

            cursor:
                pointer;

            font-size:
                11px;

            font-weight:
                800;

        }


        .secondary-success-button {

            border:
                1px solid #344052;

            background:
                #151d29;

            color:
                #8b96a8;

        }


        .primary-success-button {

            border:
                none;

            background:
                #7c83ff;

            color:
                #ffffff;

            box-shadow:
                0 8px 25px
                rgba(124,131,255,.15);

        }


        .primary-success-button:hover {

            background:
                #9298ff;

        }


        .application-message {

            position:
                fixed;

            right:
                25px;

            bottom:
                25px;

            z-index:
                5000;

            min-width:
                290px;

            padding:
                14px 16px;

            display:
                flex;

            align-items:
                center;

            gap:
                10px;

            border:
                1px solid #394355;

            border-radius:
                9px;

            background:
                #111822;

            color:
                #dce1e8;

            box-shadow:
                0 20px 60px
                rgba(0,0,0,.4);

            font-size:
                11px;

        }


        .application-message span {

            width:
                24px;

            height:
                24px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            border-radius:
                6px;

            background:
                #29171c;

            color:
                #fb7185;

            font-weight:
                900;

        }


        @media(max-width:650px) {

            .success-card {

                padding:
                    30px 20px;

            }


            .success-card h2 {

                font-size:
                    24px;

            }


            .analysis-preview {

                grid-template-columns:
                    1fr;

            }


            .analysis-preview div {

                border-right:
                    none;

                border-bottom:
                    1px solid #242d3b;

            }


            .analysis-preview div:last-child {

                border-bottom:
                    none;

            }


            .success-actions {

                width:
                    100%;

                flex-direction:
                    column;

            }


            .secondary-success-button,
            .primary-success-button {

                width:
                    100%;

            }

        }

    `;


    document.head.appendChild(
        style
    );

}
