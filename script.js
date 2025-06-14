// Existing Code (Popup and Form Switching)
const btnpopup = document.querySelector('.btnLogin-popup');
const cover_box = document.querySelector('.cover_box');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const iconClose = document.querySelector('.icon-close');
const loginForm = document.querySelector('.form-box.login');
const registerForm = document.querySelector('.form-box.register');

function showLoginForm() {
    loginForm.style.transform = "translateX(0)";
    registerForm.style.transform = "translateX(400px)";
    cover_box.classList.remove("activate");
}

function showRegisterForm() {
    registerForm.style.transform = "translateX(0)";
    loginForm.style.transform = "translateX(-400px)";
    cover_box.classList.add("activate");
}

function activatePopup() {
    cover_box.classList.add('active-popup');
}

function deactivatePopup() {
    cover_box.classList.remove('active-popup');
    showLoginForm(); // Reset to login form when closing
}

registerLink.addEventListener('click', showRegisterForm);
loginLink.addEventListener('click', showLoginForm);
btnpopup.addEventListener('click', activatePopup);
iconClose.addEventListener('click', deactivatePopup);

// New Login & Registration Handling Code
document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector(".form-box.login form");
    const registerForm = document.querySelector(".form-box.register form");

    // Handle Registration
    registerForm.addEventListener("submit", (event) => {
        event.preventDefault();
        
        const username = registerForm.querySelector("input[type='text']").value;
        const email = registerForm.querySelector("input[type='email']").value;
        const password = registerForm.querySelector("input[type='password']").value;

        if (username && email && password) {
            // Save user details to localStorage
            localStorage.setItem("userEmail", email);
            localStorage.setItem("userPassword", password);
            alert("Registration Successful! Please login.");
            showLoginForm(); // Switch to login form
        } else {
            alert("Please fill all fields.");
        }
    });

    // Handle Login
    loginForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const email = loginForm.querySelector("input[type='email']").value;
        const password = loginForm.querySelector("input[type='password']").value;

        const savedEmail = localStorage.getItem("userEmail");
        const savedPassword = localStorage.getItem("userPassword");

        if (email === savedEmail && password === savedPassword) {
            alert("Login Successful!");
            window.location.href = "http://127.0.0.1:5000/"; // Redirect to a new page
        } else {
            alert("Invalid email or password.");
        }
    });
});
