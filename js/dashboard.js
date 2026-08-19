/* =========================================================
   CHAOSPILOT — DASHBOARD JS
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    initializeDashboard();
});


/* =========================================================
   INITIALIZE
   ========================================================= */

function initializeDashboard() {

    setupNavigation();
    setupRefresh();
    setupNotifications();
    setupAddApplication();
    setupWhatIf();
    setupExampleScenarios();
    setupAIEngineer();
    setupExperiment();
    setupLogout();
    updateUser();
    loadApplicationStatus();

}


/* =========================================================
   SIDEBAR NAVIGATION
   ========================================================= */

function setupNavigation() {

    const links =
        document.querySelectorAll(".nav-item");

    links.forEach(link => {

        link.addEventListener("click", function () {

            links.forEach(item => {
                item.classList.remove("active");
            });

            this.classList.add("active");

        });

    });

}


/* =========================================================
   ADD APPLICATION
   IMPORTANT:
   This opens application.html.
   No modal here.
   ========================================================= */

function setupAddApplication() {

    const button =
        document.getElementById("addApplicationButton");

    if (!button) return;

    button.addEventListener("click", () => {

        window.location.href =
            "./application.html";

    });

}


/* =========================================================
   REFRESH
   ========================================================= */

function setupRefresh() {

    const button =
        document.getElementById("refreshButton");

    if (!button) return;

    button.addEventListener("click", () => {

        const originalText =
            button.innerHTML;

        button.disabled = true;

        button.innerHTML =
            "↻ Analyzing...";


        setTimeout(() => {

            button.disabled = false;

            button.innerHTML =
                originalText;

            showToast(
                "System analysis updated successfully",
                "success"
            );

        }, 1200);

    });

}


/* =========================================================
   NOTIFICATIONS
   ========================================================= */

function setupNotifications() {

    const button =
        document.getElementById(
            "notificationButton"
        );

    if (!button) return;

    button.addEventListener("click", () => {

        const existing =
            document.querySelector(
                ".dashboard-notifications"
            );

        if (existing) {

            existing.remove();

            return;

        }

        showNotificationPanel();

    });

}


function showNotificationPanel() {

    const panel =
        document.createElement("div");

    panel.className =
        "dashboard-notifications";

    panel.innerHTML = `

        <div class="notification-title">

            <strong>
                Notifications
            </strong>

            <button id="closeNotifications">
                ×
            </button>

        </div>


        <div class="dashboard-notification danger">

            <b>
                Critical risk
            </b>

            <p>
                Payment Service currently has
                no fallback mechanism.
            </p>

        </div>


        <div class="dashboard-notification warning">

            <b>
                Recovery warning
            </b>

            <p>
                PostgreSQL recovery time is
                above the target.
            </p>

        </div>


        <div class="dashboard-notification success">

            <b>
                Experiment completed
            </b>

            <p>
                Redis failure experiment
                completed successfully.
            </p>

        </div>

    `;

    document.body.appendChild(panel);


    document
        .getElementById("closeNotifications")
        .addEventListener("click", () => {

            panel.remove();

        });

}


/* =========================================================
   WHAT-IF ANALYSIS
   ========================================================= */

function setupWhatIf() {

    const input =
        document.getElementById(
            "whatIfInput"
        );

    const button =
        document.getElementById(
            "simulateBtn"
        );

    if (!input || !button)
        return;


    button.addEventListener("click", () => {

        const scenario =
            input.value.trim();


        if (!scenario) {

            showToast(
                "Describe a failure scenario first",
                "warning"
            );

            input.focus();

            return;

        }


        analyzeScenario(
            scenario,
            button
        );

    });


    input.addEventListener(
        "keydown",
        event => {

            if (event.key === "Enter") {

                event.preventDefault();

                button.click();

            }

        }
    );

}


/* =========================================================
   ANALYZE SCENARIO
   ========================================================= */

function analyzeScenario(
    scenario,
    button
) {

    const originalText =
        button.innerHTML;

    button.disabled = true;

    button.innerHTML =
        "Analyzing...";


    /*
     * TEMPORARY FRONTEND SIMULATION
     *
     * Later this becomes:
     *
     * POST /api/analyze
     *
     * The backend AI will perform
     * the actual analysis.
     */


    setTimeout(() => {

        button.disabled = false;

        button.innerHTML =
            originalText;


        updatePrediction(
            scenario
        );


        showToast(
            "AI failure analysis completed",
            "success"
        );

    }, 1500);

}


/* =========================================================
   EXAMPLE SCENARIOS
   ========================================================= */

function setupExampleScenarios() {

    const buttons =
        document.querySelectorAll(
            ".example-scenarios button"
        );

    const input =
        document.getElementById(
            "whatIfInput"
        );

    if (!input) return;


    buttons.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                input.value =
                    button.textContent.trim();

                input.focus();

            }
        );

    });

}


/* =========================================================
   UPDATE PREDICTION
   ========================================================= */

function updatePrediction(
    scenario
) {

    const title =
        document.querySelector(
            ".prediction-title h3"
        );

    const confidence =
        document.querySelector(
            ".prediction-confidence strong"
        );


    const text =
        scenario.toLowerCase();


    let service =
        "Payment Service";

    let confidenceValue =
        "94%";


    if (
        text.includes("database") ||
        text.includes("postgres") ||
        text.includes("sql")
    ) {

        service =
            "PostgreSQL";

        confidenceValue =
            "96%";

    }

    else if (
        text.includes("redis") ||
        text.includes("cache")
    ) {

        service =
            "Redis Cache";

        confidenceValue =
            "89%";

    }

    else if (
        text.includes("traffic") ||
        text.includes("10x") ||
        text.includes("load")
    ) {

        service =
            "API Gateway";

        confidenceValue =
            "91%";

    }

    else if (
        text.includes("payment")
    ) {

        service =
            "Payment Service";

        confidenceValue =
            "94%";

    }


    if (title) {

        title.textContent =
            service;

    }


    if (confidence) {

        confidence.textContent =
            confidenceValue;

    }

}


/* =========================================================
   AI ENGINEER
   ========================================================= */

function setupAIEngineer() {

    const button =
        document.getElementById(
            "openAIButton"
        );

    if (!button) return;


    button.addEventListener(
        "click",
        openAIEngineer
    );

}


function openAIEngineer() {

    const existing =
        document.querySelector(
            ".ai-engineer-panel"
        );


    if (existing) {

        existing.remove();

        return;

    }


    const panel =
        document.createElement("div");

    panel.className =
        "ai-engineer-panel";


    panel.innerHTML = `

        <div class="ai-panel-top">

            <div>

                <span>
                    ✦ CHAOSPILOT AI
                </span>

                <strong>
                    AI Engineer
                </strong>

            </div>


            <button id="closeAI">
                ×
            </button>

        </div>


        <div
            class="ai-panel-body"
            id="aiPanelBody"
        >

            <div class="ai-message">

                <div class="ai-avatar">
                    ✦
                </div>


                <div>

                    <strong>
                        ChaosPilot
                    </strong>


                    <p>
                        I found that Payment Service
                        currently has the highest
                        dependency impact.
                    </p>

                </div>

            </div>

        </div>


        <div class="ai-panel-input">

            <input
                id="aiInput"
                type="text"
                placeholder="Ask about your system..."
            >


            <button id="aiSend">
                →
            </button>

        </div>

    `;


    document.body.appendChild(panel);


    document
        .getElementById("closeAI")
        .addEventListener(
            "click",
            () => {

                panel.remove();

            }
        );


    document
        .getElementById("aiSend")
        .addEventListener(
            "click",
            sendAIMessage
        );


    document
        .getElementById("aiInput")
        .addEventListener(
            "keydown",
            event => {

                if (event.key === "Enter") {

                    sendAIMessage();

                }

            }
        );

}


/* =========================================================
   AI CHAT
   ========================================================= */

function sendAIMessage() {

    const input =
        document.getElementById(
            "aiInput"
        );

    const body =
        document.getElementById(
            "aiPanelBody"
        );


    if (!input || !body)
        return;


    const question =
        input.value.trim();


    if (!question)
        return;


    const userMessage =
        document.createElement("div");


    userMessage.className =
        "user-ai-message";


    userMessage.textContent =
        question;


    body.appendChild(
        userMessage
    );


    input.value = "";


    body.scrollTop =
        body.scrollHeight;


    setTimeout(() => {

        const response =
            document.createElement("div");


        response.className =
            "ai-message";


        response.innerHTML = `

            <div class="ai-avatar">
                ✦
            </div>

            <div>

                <strong>
                    ChaosPilot
                </strong>

                <p>
                    Based on the current system model,
                    I recommend checking service
                    dependencies and failure recovery
                    paths before running a production
                    experiment.
                </p>

            </div>

        `;


        body.appendChild(
            response
        );


        body.scrollTop =
            body.scrollHeight;


    }, 800);

}


/* =========================================================
   RUN EXPERIMENT
   ========================================================= */

function setupExperiment() {

    const button =
        document.getElementById(
            "runExperimentButton"
        );

    if (!button) return;


    button.addEventListener(
        "click",
        showExperimentModal
    );

}


function showExperimentModal() {

    const modal =
        createModal(`

            <span class="modal-eyebrow">
                CHAOS ENGINEERING
            </span>


            <h2>
                Run controlled experiment
            </h2>


            <p>
                Select a failure scenario to
                test application resilience.
            </p>


            <label>
                FAILURE SCENARIO
            </label>


            <select id="experimentType">

                <option>
                    Payment Service Failure
                </option>

                <option>
                    Database Failure
                </option>

                <option>
                    API Timeout
                </option>

                <option>
                    Redis Failure
                </option>

            </select>


            <div class="experiment-warning">

                ⚠ Only run experiments against
                systems you are authorized to test.

            </div>


            <div class="modal-actions">

                <button
                    class="modal-secondary"
                    id="cancelExperiment"
                >
                    Cancel
                </button>


                <button
                    class="modal-primary"
                    id="startExperiment"
                >
                    Start Experiment
                </button>

            </div>

        `);


    modal
        .querySelector("#cancelExperiment")
        .addEventListener(
            "click",
            () => {

                modal.remove();

            }
        );


    modal
        .querySelector("#startExperiment")
        .addEventListener(
            "click",
            () => {

                const experiment =
                    document
                        .getElementById(
                            "experimentType"
                        )
                        .value;


                modal.remove();


                showToast(
                    `${experiment} experiment started`,
                    "success"
                );

            }
        );

}


/* =========================================================
   CREATE MODAL
   ========================================================= */

function createModal(
    content
) {

    const overlay =
        document.createElement("div");


    overlay.className =
        "dashboard-modal-overlay";


    overlay.innerHTML = `

        <div class="dashboard-modal">

            <button
                class="modal-close"
                type="button"
            >
                ×
            </button>


            ${content}

        </div>

    `;


    document.body.appendChild(
        overlay
    );


    overlay
        .querySelector(".modal-close")
        .addEventListener(
            "click",
            () => {

                overlay.remove();

            }
        );


    overlay.addEventListener(
        "click",
        event => {

            if (
                event.target === overlay
            ) {

                overlay.remove();

            }

        }
    );


    return overlay;

}


/* =========================================================
   LOGOUT
   ========================================================= */

function setupLogout() {

    const button =
        document.getElementById(
            "logoutButton"
        );


    if (!button) return;


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
   USER
   ========================================================= */

function updateUser() {

    const stored =
        localStorage.getItem(
            "chaospilot_user"
        );


    if (!stored)
        return;


    try {

        const user =
            JSON.parse(stored);


        const name =
            document.querySelector(
                ".sidebar-user strong"
            );


        if (
            name &&
            user.name
        ) {

            name.textContent =
                user.name;

        }

    }

    catch {

        console.log(
            "User profile unavailable."
        );

    }

}


/* =========================================================
   APPLICATION STATUS
   ========================================================= */

function loadApplicationStatus() {

    const stored =
        localStorage.getItem(
            "chaospilot_application"
        );


    if (!stored)
        return;


    try {

        const application =
            JSON.parse(stored);


        /*
         * Later this data will come
         * from the backend database.
         */


        const workspaceName =
            document.querySelector(
                ".workspace-select strong"
            );


        if (
            workspaceName &&
            application.name
        ) {

            workspaceName.textContent =
                application.name;

        }


        console.log(
            "Connected application:",
            application
        );

    }

    catch {

        console.log(
            "Application data unavailable."
        );

    }

}


/* =========================================================
   TOAST
   ========================================================= */

function showToast(
    message,
    type = "info"
) {

    const existing =
        document.querySelector(
            ".dashboard-toast"
        );


    if (existing)
        existing.remove();


    const toast =
        document.createElement("div");


    toast.className =
        `dashboard-toast ${type}`;


    let icon = "●";


    if (type === "success") {

        icon = "✓";

    }

    else if (type === "warning") {

        icon = "!";

    }


    toast.innerHTML = `

        <span>
            ${icon}
        </span>

        <p>
            ${escapeHTML(message)}
        </p>

    `;


    document.body.appendChild(
        toast
    );


    setTimeout(() => {

        toast.classList.add("hide");


        setTimeout(() => {

            toast.remove();

        }, 300);

    }, 2500);

}


/* =========================================================
   ESCAPE HTML
   ========================================================= */

function escapeHTML(
    value
) {

    const element =
        document.createElement("div");


    element.textContent =
        value;


    return element.innerHTML;

}