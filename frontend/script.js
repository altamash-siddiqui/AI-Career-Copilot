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
// LOGIN
// ============================================================

async function loginUser() {

    const username = usernameInput
        ? usernameInput.value.trim()
        : "";

    const password = passwordInput
        ? passwordInput.value.trim()
        : "";

    if (!username || !password) {

        alert(
            "Please enter your username and password."
        );

        return;
    }

    // Disable button during request

    if (loginButton) {

        loginButton.disabled = true;

        loginButton.innerText =
            "CONNECTING...";
    }

    try {

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

        if (result.success) {

            // Save logged-in user

            localStorage.setItem(
                "careerCopilotUser",
                result.username
            );

            alert(
                `Welcome back, ${result.username}! 🚀`
            );

            console.log(
                "Login successful:",
                result
            );

            // For now keep the user on the
            // same page. Dashboard connection
            // will be added next.

            window.location.href = "dashboard.html";

        } else {

            alert(
                result.message ||
                "Invalid username or password."
            );
        }

    } catch (error) {

        console.error(
            "Login error:",
            error
        );

        alert(
            "Unable to connect to AI Career Copilot server."
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

    if (!username) {
        return;
    }

    const password = prompt(
        "Create your password:"
    );

    if (!password) {
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/api/register`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    username: username.trim(),
                    password: password.trim()
                })
            }
        );

        const result = await response.json();

        if (result.success) {

            alert(
                "Account created successfully! 🚀\n\n" +
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

        } else {

            alert(
                result.message ||
                "Registration failed."
            );
        }

    } catch (error) {

        console.error(
            "Registration error:",
            error
        );

        alert(
            "Unable to connect to AI Career Copilot server."
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

            if (
                event.key === "Enter"
            ) {

                loginUser();
            }
        }
    );
}


// ============================================================
// SYSTEM READY
// ============================================================

console.log(
    "🤖 AI Career Copilot frontend connected."
);

console.log(
    "🔗 Backend:",
    API_URL
);

// ============================================================
// PASSWORD SHOW / HIDE
// ============================================================

const passwordToggle = document.getElementById("passwordToggle");
const passwordField = document.getElementById("password");

if (passwordToggle && passwordField) {

    passwordToggle.addEventListener("click", function () {

        if (passwordField.type === "password") {

            passwordField.type = "text";
            passwordToggle.innerText = "◉";

        } else {

            passwordField.type = "password";
            passwordToggle.innerText = "◉";

        }

    });

}