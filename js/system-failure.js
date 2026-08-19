/* =========================================================
   CHAOSPILOT — SYSTEM FAILURE ANALYSIS
   ========================================================= */

document.addEventListener("DOMContentLoaded", initializeFailurePage);


/* =========================================================
   INITIALIZATION
   ========================================================= */

function initializeFailurePage() {

    loadApplication();

    setupComponents();

    setupSimulation();

    setupBackButton();

    setupRecommendation();

    setupExperiment();

    setupCopyCode();

    setupLogout();

}


/* =========================================================
   DEMO FAILURE DATA
   ========================================================= */

const failureData = {

    "Payment Service": {

        confidence: "94%",
        blast: 43,
        impact: "HIGH",
        recovery: "18 min",

        description:
            "Users may be unable to complete checkout and payment operations.",

        file:
            "payment_service.py",

        function:
            "process_payment()",

        line:
            142,

        severity:
            "CRITICAL",

        codeFile:
            "backend/payment_service.py",

        codeLines: [
            {
                line: 139,
                code: "payment = create_payment(data)"
            },
            {
                line: 140,
                code: ""
            },
            {
                line: 141,
                code: "# Process database transaction"
            },
            {
                line: 142,
                code: "result = db.execute(payment_query)",
                error: true
            },
            {
                line: 143,
                code: ""
            },
            {
                line: 144,
                code: "return result"
            },
            {
                line: 145,
                code: ""
            },
            {
                line: 146,
                code: "send_confirmation(payment)"
            }
        ],

        explanation:
            "The database operation can throw a timeout exception, but process_payment() does not handle the exception. When the database becomes slow or unavailable, the exception propagates to the API layer and produces a 500 response.",

        recommendation:
            "Add database timeout handling",

        recommendationText:
            "Introduce timeout handling, controlled retries and a fallback strategy around the database operation to prevent the exception from reaching the API layer."

    },


    "PostgreSQL": {

        confidence: "97%",
        blast: 78,
        impact: "CRITICAL",
        recovery: "32 min",

        description:
            "Most transactional operations may become unavailable when the primary database cannot accept requests.",

        file:
            "database.py",

        function:
            "get_connection()",

        line:
            87,

        severity:
            "CRITICAL",

        codeFile:
            "backend/database.py",

        codeLines: [
            {
                line: 84,
                code: "def get_connection():"
            },
            {
                line: 85,
                code: "    connection = create_connection()"
            },
            {
                line: 86,
                code: ""
            },
            {
                line: 87,
                code: "    return connection",
                error: true
            },
            {
                line: 88,
                code: ""
            },
            {
                line: 89,
                code: "def close_connection(connection):"
            }
        ],

        explanation:
            "The application depends on a single database connection path. When the database becomes unavailable, connection errors propagate to dependent services without an automated failover mechanism.",

        recommendation:
            "Introduce database failover",

        recommendationText:
            "Use replication, health checks and automated failover so dependent services can recover when the primary database becomes unavailable."

    },


    "API Gateway": {

        confidence: "98%",
        blast: 91,
        impact: "CRITICAL",
        recovery: "25 min",

        description:
            "Most external requests may fail while the API Gateway is unavailable.",

        file:
            "gateway.py",

        function:
            "forward_request()",

        line:
            214,

        severity:
            "CRITICAL",

        codeFile:
            "backend/gateway.py",

        codeLines: [
            {
                line: 211,
                code: "def forward_request(request):"
            },
            {
                line: 212,
                code: "    target = resolve_service(request)"
            },
            {
                line: 213,
                code: ""
            },
            {
                line: 214,
                code: "    return requests.post(target)",
                error: true
            },
            {
                line: 215,
                code: ""
            },
            {
                line: 216,
                code: "    log_request(request)"
            }
        ],

        explanation:
            "The gateway forwards requests through a single critical path. If the downstream routing operation fails and no fallback gateway exists, incoming requests immediately fail.",

        recommendation:
            "Deploy gateway redundancy",

        recommendationText:
            "Use multiple gateway instances with health checks, load balancing and automated failover."

    },


    "Order Service": {

        confidence: "92%",
        blast: 51,
        impact: "HIGH",
        recovery: "21 min",

        description:
            "New orders may remain pending or fail to complete.",

        file:
            "order_service.py",

        function:
            "create_order()",

        line:
            87,

        severity:
            "HIGH",

        codeFile:
            "backend/order_service.py",

        codeLines: [
            {
                line: 84,
                code: "def create_order(data):"
            },
            {
                line: 85,
                code: "    payment = get_payment(data)"
            },
            {
                line: 86,
                code: ""
            },
            {
                line: 87,
                code: "    order = payment.create_order()",
                error: true
            },
            {
                line: 88,
                code: ""
            },
            {
                line: 89,
                code: "    save_order(order)"
            }
        ],

        explanation:
            "Order creation depends directly on another service without a durable retry mechanism. Temporary dependency failures can therefore leave orders incomplete.",

        recommendation:
            "Introduce asynchronous order processing",

        recommendationText:
            "Use a durable queue and retry mechanism so temporary service failures do not lose customer requests."

    },


    "Redis Cache": {

        confidence: "89%",
        blast: 18,
        impact: "LOW",
        recovery: "7 min",

        description:
            "The application may remain available but response times could increase.",

        file:
            "cache_service.py",

        function:
            "get_cached_data()",

        line:
            63,

        severity:
            "MEDIUM",

        codeFile:
            "backend/cache_service.py",

        codeLines: [
            {
                line: 60,
                code: "def get_cached_data(key):"
            },
            {
                line: 61,
                code: "    cache = redis_client()"
            },
            {
                line: 62,
                code: ""
            },
            {
                line: 63,
                code: "    return cache.get(key)",
                error: true
            },
            {
                line: 64,
                code: ""
            },
            {
                line: 65,
                code: "    return database.get(key)"
            }
        ],

        explanation:
            "The cache access path does not gracefully degrade when Redis becomes unavailable. Requests may wait for the failed cache operation instead of immediately falling back to the database.",

        recommendation:
            "Add cache degradation handling",

        recommendationText:
            "Allow services to bypass Redis and use the primary data source when the cache is unavailable."

    },


    "Notification Service": {

        confidence: "87%",
        blast: 12,
        impact: "LOW",
        recovery: "5 min",

        description:
            "Core transactions should continue, but notifications may be delayed.",

        file:
            "notification_service.py",

        function:
            "send_notification()",

        line:
            118,

        severity:
            "MEDIUM",

        codeFile:
            "backend/notification_service.py",

        codeLines: [
            {
                line: 115,
                code: "def send_notification(user, message):"
            },
            {
                line: 116,
                code: "    notification = build_message(message)"
            },
            {
                line: 117,
                code: ""
            },
            {
                line: 118,
                code: "    notification.send(user)",
                error: true
            },
            {
                line: 119,
                code: ""
            },
            {
                line: 120,
                code: "    return True"
            }
        ],

        explanation:
            "Notification delivery is executed synchronously with the main workflow. A notification failure can therefore delay the operation that should remain independent.",

        recommendation:
            "Decouple notifications from transactions",

        recommendationText:
            "Process notifications asynchronously so notification failures cannot block core transactions."

    }

};


/* =========================================================
   APPLICATION
   ========================================================= */

function loadApplication() {

    const stored =
        localStorage.getItem("chaospilot_application");

    if (!stored) return;

    try {

        const application = JSON.parse(stored);

        const workspace =
            document.getElementById("workspaceName");

        if (
            workspace &&
            application.name
        ) {
            workspace.textContent =
                application.name;
        }

    } catch (error) {

        console.log(
            "Application information unavailable."
        );

    }
}


/* =========================================================
   COMPONENT SELECTION
   ========================================================= */

function setupComponents() {

    const components =
        document.querySelectorAll(".component-card");

    components.forEach(component => {

        component.addEventListener("click", () => {

            components.forEach(item => {

                item.classList.remove("selected");

            });

            component.classList.add("selected");

            const name =
                component.dataset.component;

            updateFailureAnalysis(name);

        });

    });

}


/* =========================================================
   UPDATE FAILURE ANALYSIS
   ========================================================= */

function updateFailureAnalysis(component) {

    const data =
        failureData[component];

    if (!data) return;


    setText(
        "failureTitle",
        `${component} Failure`
    );


    setText(
        "failureDescription",
        data.description
    );


    setText(
        "chainStart",
        component
    );


    setText(
        "confidenceValue",
        data.confidence
    );


    setText(
        "blastValue",
        data.blast
    );


    setText(
        "impactLevel",
        data.impact
    );


    setText(
        "recoveryTime",
        data.recovery
    );


    setText(
        "impactDescription",
        data.description
    );


    setText(
        "rootFile",
        data.file
    );


    setText(
        "rootFunction",
        data.function
    );


    setText(
        "rootLine",
        data.line
    );


    setText(
        "rootSeverity",
        data.severity
    );


    setText(
        "codeFile",
        data.codeFile
    );


    setText(
        "rootExplanation",
        data.explanation
    );


    setText(
        "recommendationTitle",
        data.recommendation
    );


    setText(
        "recommendationText",
        data.recommendationText
    );


    const blastBar =
        document.getElementById("blastBar");

    if (blastBar) {

        blastBar.style.width =
            `${data.blast}%`;

    }


    renderCode(data);

}


/* =========================================================
   RENDER CODE
   ========================================================= */

function renderCode(data) {

    const codeElement =
        document.getElementById("codeSnippet");

    if (!codeElement) return;


    codeElement.innerHTML =
        data.codeLines
            .map(item => {

                const lineClass =
                    item.error
                        ? "line-number error-line"
                        : "line-number";

                return `
<span class="${lineClass}">
${item.line}
</span>${escapeHTML(item.code)}
`;

            })
            .join("\n");

}


/* =========================================================
   SIMULATE FAILURE
   ========================================================= */

function setupSimulation() {

    const button =
        document.getElementById("simulateFailure");

    if (!button) return;


    button.addEventListener("click", () => {

        const selected =
            document.querySelector(
                ".component-card.selected"
            );


        if (!selected) {

            showToast(
                "Please select a component first.",
                "warning"
            );

            return;

        }


        const component =
            selected.dataset.component;


        button.disabled = true;

        button.innerHTML =
            "⚡ Tracing failure path...";


        const originalText =
            button.innerHTML;


        setTimeout(() => {

            button.disabled = false;

            button.innerHTML =
                '<span>⚡</span> Analyze Failure';


            showToast(
                `Root cause analysis completed for ${component}.`,
                "success"
            );


            revealAnalysis();

        }, 1600);

    });

}


/* =========================================================
   REVEAL RESULT
   ========================================================= */

function revealAnalysis() {

    const result =
        document.getElementById("analysisResult");

    if (!result) return;


    result.classList.add("visible");


    result.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}


/* =========================================================
   COPY CODE
   ========================================================= */

function setupCopyCode() {

    const button =
        document.getElementById("copyCode");

    if (!button) return;


    button.addEventListener("click", async () => {

        const code =
            document.getElementById("codeSnippet");

        if (!code) return;


        try {

            await navigator.clipboard.writeText(
                code.innerText
            );


            const original =
                button.textContent;


            button.textContent =
                "Copied ✓";


            setTimeout(() => {

                button.textContent =
                    original;

            }, 1500);

        } catch {

            showToast(
                "Could not copy code.",
                "warning"
            );

        }

    });

}


/* =========================================================
   BACK TO DASHBOARD
   ========================================================= */

function setupBackButton() {

    const button =
        document.getElementById("backButton");

    if (!button) return;


    button.addEventListener("click", () => {

        window.location.href =
            "./dashboard.html";

    });

}


/* =========================================================
   AI RECOMMENDATION
   ========================================================= */

function setupRecommendation() {

    const button =
        document.getElementById(
            "viewRecommendation"
        );

    if (!button) return;


    button.addEventListener("click", () => {

        const selected =
            document.querySelector(
                ".component-card.selected"
            );


        const component =
            selected
                ? selected.dataset.component
                : "Payment Service";


        const data =
            failureData[component];


        showModal(`

            <span class="modal-eyebrow">
                CHAOSPILOT AI FIX
            </span>

            <h2>
                ${escapeHTML(
                    data.recommendation
                )}
            </h2>

            <p>
                ${escapeHTML(
                    data.recommendationText
                )}
            </p>

            <div class="fix-list">

                <div>
                    ✓ Add failure handling
                </div>

                <div>
                    ✓ Add controlled retry
                </div>

                <div>
                    ✓ Add fallback behaviour
                </div>

                <div>
                    ✓ Validate recovery with tests
                </div>

            </div>

            <div class="modal-actions">

                <button
                    class="modal-primary"
                    id="closeFix"
                >
                    Close
                </button>

            </div>

        `);


        document
            .getElementById("closeFix")
            ?.addEventListener(
                "click",
                closeModal
            );

    });

}


/* =========================================================
   CONTROLLED EXPERIMENT
   ========================================================= */

function setupExperiment() {

    const button =
        document.getElementById(
            "runExperiment"
        );

    if (!button) return;


    button.addEventListener("click", () => {

        const selected =
            document.querySelector(
                ".component-card.selected"
            );


        const component =
            selected
                ? selected.dataset.component
                : "selected component";


        showModal(`

            <span class="modal-eyebrow">
                CONTROLLED CHAOS EXPERIMENT
            </span>

            <h2>
                Test ${escapeHTML(component)}
            </h2>

            <p>
                ChaosPilot will prepare a controlled
                experiment based on the predicted
                failure path.
            </p>

            <div class="experiment-warning">

                ⚠ This frontend prototype does not
                actually disrupt production systems.

                Real experiments will require backend
                safety controls and explicit authorization.

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
                    id="prepareExperiment"
                >
                    Prepare Experiment
                </button>

            </div>

        `);


        document
            .getElementById("cancelExperiment")
            ?.addEventListener(
                "click",
                closeModal
            );


        document
            .getElementById("prepareExperiment")
            ?.addEventListener(
                "click",
                () => {

                    closeModal();

                    showToast(
                        "Experiment prepared successfully.",
                        "success"
                    );

                }
            );

    });

}


/* =========================================================
   MODAL
   ========================================================= */

function showModal(content) {

    closeModal();


    const overlay =
        document.createElement("div");


    overlay.className =
        "modal-overlay";


    overlay.innerHTML = `

        <div class="modal-box">

            <button
                class="modal-close"
                id="modalClose"
            >
                ×
            </button>

            ${content}

        </div>

    `;


    document.body.appendChild(
        overlay
    );


    document
        .getElementById("modalClose")
        ?.addEventListener(
            "click",
            closeModal
        );


    overlay.addEventListener(
        "click",
        event => {

            if (
                event.target === overlay
            ) {

                closeModal();

            }

        }
    );

}


function closeModal() {

    const modal =
        document.querySelector(
            ".modal-overlay"
        );


    if (modal) {

        modal.remove();

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

    if (!button) return;


    button.addEventListener("click", () => {

        localStorage.removeItem(
            "chaospilot_user"
        );

        localStorage.removeItem(
            "chaospilot_logged_in"
        );

        window.location.href =
            "./login.html";

    });

}


/* =========================================================
   TOAST
   ========================================================= */

function showToast(
    message,
    type = "info"
) {

    const oldToast =
        document.querySelector(
            ".failure-toast"
        );


    if (oldToast) {

        oldToast.remove();

    }


    const toast =
        document.createElement("div");


    toast.className =
        "failure-toast";


    toast.innerHTML = `

        <span>
            ${
                type === "success"
                    ? "✓"
                    : "!"
            }
        </span>

        <p>
            ${escapeHTML(message)}
        </p>

    `;


    document.body.appendChild(
        toast
    );


    setTimeout(() => {

        toast.remove();

    }, 3000);

}


/* =========================================================
   HELPER
   ========================================================= */

function setText(
    id,
    value
) {

    const element =
        document.getElementById(id);

    if (element) {

        element.textContent =
            value;

    }

}


/* =========================================================
   ESCAPE HTML
   ========================================================= */

function escapeHTML(value) {

    const element =
        document.createElement("div");

    element.textContent =
        value;

    return element.innerHTML;

}