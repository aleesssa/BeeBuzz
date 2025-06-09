function validateForm() {
    var password = document.getElementById("pwd").value;
    var confirmPassword = document.getElementById("confirm_password").value;
    var errorMessage = document.getElementById("error-message");

    var passwordRegex = /^(?=.*[0-9])(?=.{8,})/;
    if (!passwordRegex.test(password)) {
        errorMessage.textContent = "Password must be at least 8 characters long and contain a number.";
        return false;
    }

    if(password !== confirmPassword) {
        errorMessage.textContent = "Passwords do not match!";
        return false;
    }

    errorMessage.textContent = "";
    return true;
    
}

document.addEventListener("DOMContentLoaded", function() {
    const password = document.getElementById("pwd");
    const confirmPassword = document.getElementById("confirm_password");

    // Double click password to toggle
    password.addEventListener("dblclick", function() {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
    });

    // Double click confirm password to toggle
    confirmPassword.addEventListener("dblclick", function() {
        const type = confirmPassword.getAttribute('type') === 'password' ? 'text' : 'password';
        confirmPassword.setAttribute('type', type);
    });
});

const loginForm = document.getElementById('loginForm');

loginForm.addEventListener('submit', function(event) {
    
    const userInput = document.getElementById('userInput').value;
    const password = document.getElementById('pwd').value;

    if (userInput.includes('@')) {
        console.log('Logging in using Email:', userInput);
    } else {
        console.log('Logging in using Username:', userInput);
    }

});


