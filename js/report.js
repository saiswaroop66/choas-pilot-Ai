/* =========================================================
   CHAOSPILOT — REPORT JS
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    initializeReport
);


/* =========================================================
   INITIALIZE
   ========================================================= */

function initializeReport() {

    loadApplication();

    setReportDate();

    setupDashboardButton();

    setupRefresh();

    setupDownload();

    setupNewAnalysis();

    setupLogout();

    animateScore();

}


/* =========================================================
   LOAD APPLICATION
   ========================================================= */

function loadApplication() {

    const stored =
        localStorage.getItem(
            "chaospilot_application"
        );


    if (!stored) return;


    try {

        const application =
            JSON.parse(stored);


        const workspace =
            document.getElementById(
                "workspaceName"
            );


        const reportApplication =
            document.getElementById(
                "reportApplication"
            );


        if (
            application.name &&
            workspace
        ) {

            workspace.textContent =
                application.name;

        }


        if (
            application.name &&
            reportApplication
        ) {

            reportApplication.textContent =
                application.name;

        }

    } catch (error) {

        console.log(
            "Application information unavailable."
        );

    }

}


/* =========================================================
   DATE
   ========================================================= */

function setReportDate() {

    const dateElement =
        document.getElementById(
            "reportDate"
        );


    if (!dateElement) return;


    const today =
        new Date();


    dateElement.textContent =
        today.toLocaleDateString(
            "en-US",
            {
                year: "numeric",
                month: "long",
                day: "numeric"
            }
        );

}


/* =========================================================
   DASHBOARD
   ========================================================= */

function setupDashboardButton() {

    const button =
        document.getElementById(
            "dashboardButton"
        );


    if (!button) return;


    button.addEventListener(
        "click",
        () => {

            window.location.href =
                "./dashboard.html";

        }
    );

}


/* =========================================================
   REFRESH REPORT
   ========================================================= */

function setupRefresh() {

    const button =
        document.getElementById(
            "refreshReport"
        );


    if (!button) return;


    button.addEventListener(
        "click",
        () => {

            const originalText =
                button.innerHTML;


            button.disabled = true;

            button.innerHTML =
                "↻ Analyzing...";


            setTimeout(() => {

                button.disabled = false;

                button.innerHTML =
                    originalText;


                animateScore();


                showToast(
                    "Resilience report updated successfully.",
                    "success"
                );

            }, 1200);

        }
    );

}


/* =========================================================
   SCORE ANIMATION
   ========================================================= */

function animateScore() {

    const scoreElement =
        document.getElementById(
            "resilienceScore"
        );


    if (!scoreElement) return;


    const target =
        72;


    let current = 0;


    scoreElement.textContent =
        "0";


    const interval =
        setInterval(() => {

            current += 2;


            if (current >= target) {

                current = target;

                clearInterval(interval);

            }


            scoreElement.textContent =
                current;

        }, 20);

}


/* =========================================================
   DOWNLOAD REPORT
   ========================================================= */

function setupDownload() {

    const button =
        document.getElementById(
            "downloadReport"
        );


    if (!button) return;


    button.addEventListener(
        "click",
        () => {

            generateReportFile();

        }
    );

}


/* =========================================================
   GENERATE REPORT
   ========================================================= */

function generateReportFile() {

    const application =
        getApplicationName();


    const date =
        new Date()
            .toLocaleDateString(
                "en-US"
            );


    const report = `

CHAOSPILOT
ENGINEERING RESILIENCE REPORT
==========================================

Application:
${application}

Environment:
Production

Generated:
${date}


OVERALL RESILIENCE
------------------------------------------

Score: 72 / 100
AI Confidence: 94%


SYSTEM RISK OVERVIEW
------------------------------------------

PostgreSQL
Risk: CRITICAL
Blast Radius: 78%
Recovery: 32 minutes

API Gateway
Risk: CRITICAL
Blast Radius: 91%
Recovery: 25 minutes

Payment Service
Risk: HIGH
Blast Radius: 43%
Recovery: 18 minutes

Order Service
Risk: MEDIUM
Blast Radius: 51%
Recovery: 21 minutes

Redis Cache
Risk: LOW
Blast Radius: 18%
Recovery: 7 minutes


AI ENGINEERING SUMMARY
------------------------------------------

ChaosPilot identified three high-impact
failure paths.

The highest risks originate from the
API Gateway and PostgreSQL.

Payment Service also represents a
significant dependency for checkout.


RECOMMENDED IMPROVEMENTS
------------------------------------------

1. Introduce database failover.

2. Add gateway redundancy.

3. Improve payment fallback.

4. Increase automated recovery testing.


CHAOS EXPERIMENTS
------------------------------------------

Redis Failure: PASSED

Payment Timeout: DEGRADED

Notification Failure: PASSED


==========================================
Generated by ChaosPilot
AI-powered resilience intelligence
==========================================

`;


    const blob =
        new Blob(
            [report],
            {
                type:
                    "text/plain;charset=utf-8"
            }
        );


    const url =
        URL.createObjectURL(
            blob
        );


    const link =
        document.createElement(
            "a"
        );


    link.href =
        url;


    link.download =
        `ChaosPilot-Report-${Date.now()}.txt`;


    document.body.appendChild(
        link
    );


    link.click();


    link.remove();


    URL.revokeObjectURL(
        url
    );


    showToast(
        "Engineering report exported successfully.",
        "success"
    );

}


/* =========================================================
   APPLICATION NAME
   ========================================================= */

function getApplicationName() {

    const stored =
        localStorage.getItem(
            "chaospilot_application"
        );


    if (!stored) {

        return "ShopEasy";

    }


    try {

        const application =
            JSON.parse(stored);


        return (
            application.name ||
            "ShopEasy"
        );

    } catch {

        return "ShopEasy";

    }

}


/* =========================================================
   NEW ANALYSIS
   ========================================================= */

function setupNewAnalysis() {

    const button =
        document.getElementById(
            "runAnalysis"
        );


    if (!button) return;


    button.addEventListener(
        "click",
        () => {

            window.location.href =
                "./analysis.html";

        }
    );

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
   TOAST
   ========================================================= */

function showToast(
    message,
    type = "info"
) {

    const existing =
        document.querySelector(
            ".report-toast"
        );


    if (existing) {

        existing.remove();

    }


    const toast =
        document.createElement(
            "div"
        );


    toast.className =
        "report-toast";


    toast.innerHTML = `

        <span>
            ${type === "success" ? "✓" : "!"}
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