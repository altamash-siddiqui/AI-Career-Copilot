// ============================================================
// AI CAREER COPILOT - FRONTEND API CONNECTION
// ============================================================

const API_URL = "http://127.0.0.1:5000";

// ============================================================
// FIND LOGIN ELEMENTS
// ============================================================

const inputs = document.querySelectorAll("input");

const usernameInput = inputs[0];
const passwordInput = inputs[1];

const buttons = document.querySelectorAll("button");

let loginButton = null;
let registerButton = null;

buttons.forEach((button) => {

    const text = button.innerText
        .trim()
        .toLowerCase();

    if (
        text.includes("enter copilot") ||
        text.includes("login") ||
        text.includes("sign in")
    ) {
        loginButton = button;
    }

    if (
        text.includes("create new account") ||
        text.includes("register") ||
        text.includes("sign up")
    ) {
        registerButton = button;
    }

});

// ============================================================
// CHECK BACKEND CONNECTION
// ============================================================

async function checkBackendConnection() {

    try {

        const response = await fetch(
            `${API_URL}/api/status`
        );

        const result = await response.json();

        if (result.success) {

            console.log(
                "✅ Backend connected:",
                result.message
            );

            return true;
        }

        return false;

    } catch (error) {

        console.error(
            "❌ Backend connection failed:",
            error
        );

        return false;
    }
}

// ============================================================
// LOGIN
// ============================================================

async function loginUser() {

    const username = usernameInput
        ? usernameInput.value.trim()
        : "";

    const password = passwordInput
        ? passwordInput.value.trim()
        : "";

    // --------------------------------------------------------
    // VALIDATION
    // --------------------------------------------------------

    if (!username || !password) {

        alert(
            "Please enter your username and password."
        );

        return;
    }

    // --------------------------------------------------------
    // DISABLE LOGIN BUTTON
    // --------------------------------------------------------

    if (loginButton) {

        loginButton.disabled = true;

        loginButton.innerText =
            "CONNECTING...";
    }

    try {

        console.log(
            "🔐 Attempting login for:",
            username
        );

        const response = await fetch(
            `${API_URL}/api/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    password: password
                })
            }
        );

        const result = await response.json();

        console.log(
            "Login response:",
            result
        );

        // ----------------------------------------------------
        // SUCCESS
        // ----------------------------------------------------

        if (result.success) {

            const loggedInUsername =
                result.username || username;

            // Save user session
            localStorage.setItem(
                "careerCopilotUser",
                loggedInUsername
            );

            localStorage.setItem(
                "careerCopilotLoggedIn",
                "true"
            );

            alert(
                `Welcome back, ${loggedInUsername}! 🚀`
            );

            // Redirect to dashboard
            window.location.href =
                "dashboard.html";

        }

        // ----------------------------------------------------
        // FAILED LOGIN
        // ----------------------------------------------------

        else {

            alert(
                result.message ||
                "Invalid username or password."
            );
        }

    } catch (error) {

        console.error(
            "❌ Login error:",
            error
        );

        alert(
            "Unable to connect to AI Career Copilot server.\n\n" +
            "Make sure the Flask backend is running."
        );

    } finally {

        if (loginButton) {

            loginButton.disabled = false;

            loginButton.innerText =
                "ENTER COPILOT →";
        }
    }
}

// ============================================================
// REGISTER
// ============================================================

async function registerUser() {

    const username = prompt(
        "Create your username:"
    );

    if (!username || !username.trim()) {

        return;
    }

    const password = prompt(
        "Create your password:"
    );

    if (!password || !password.trim()) {

        return;
    }

    try {

        console.log(
            "📝 Registering user:",
            username.trim()
        );

        const response = await fetch(
            `${API_URL}/api/register`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    username:
                        username.trim(),

                    password:
                        password.trim()

                })
            }
        );

        const result =
            await response.json();

        console.log(
            "Registration response:",
            result
        );

        // ----------------------------------------------------
        // REGISTRATION SUCCESS
        // ----------------------------------------------------

        if (result.success) {

            alert(
                "✅ Account created successfully!\n\n" +
                "You can now login."
            );

            if (usernameInput) {

                usernameInput.value =
                    username.trim();
            }

            if (passwordInput) {

                passwordInput.value =
                    "";
            }

        }

        // ----------------------------------------------------
        // REGISTRATION FAILED
        // ----------------------------------------------------

        else {

            alert(
                result.message ||
                "Registration failed."
            );
        }

    } catch (error) {

        console.error(
            "❌ Registration error:",
            error
        );

        alert(
            "Unable to connect to AI Career Copilot server.\n\n" +
            "Make sure the Flask backend is running."
        );
    }
}

// ============================================================
// BUTTON EVENTS
// ============================================================

if (loginButton) {

    loginButton.addEventListener(
        "click",
        loginUser
    );
}

if (registerButton) {

    registerButton.addEventListener(
        "click",
        registerUser
    );
}

// ============================================================
// ENTER KEY LOGIN
// ============================================================

if (passwordInput) {

    passwordInput.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Enter") {

                event.preventDefault();

                loginUser();
            }

        }
    );
}

// ============================================================
// PASSWORD SHOW / HIDE
// ============================================================

const passwordToggle =
    document.getElementById(
        "passwordToggle"
    );

const passwordField =
    document.getElementById(
        "password"
    );

if (
    passwordToggle &&
    passwordField
) {

    passwordToggle.addEventListener(
        "click",
        function () {

            if (
                passwordField.type ===
                "password"
            ) {

                passwordField.type =
                    "text";

                passwordToggle.innerText =
                    "◉";

            } else {

                passwordField.type =
                    "password";

                passwordToggle.innerText =
                    "◉";
            }

        }
    );
}

// ============================================================
// SYSTEM READY
// ============================================================

console.log(
    "🤖 AI Career Copilot frontend loaded."
);

console.log(
    "🔗 Backend API:",
    API_URL
);

// ============================================================
// CHECK BACKEND WHEN PAGE LOADS
// ============================================================

checkBackendConnection()
    .then((connected) => {

        if (connected) {

            console.log(
                "🟢 AI Career Copilot system ONLINE."
            );

        } else {

            console.warn(
                "🔴 AI Career Copilot backend OFFLINE."
            );
        }

    });