function validateForm() {
    var password = document.getElementById("pwd").value;
    var confirmPassword = document.getElementById("confirm_password").value;
    var errorMessage = document.getElementById("error-message").value;

    if(password !== confirmPassword) {
        errorMessage.textContent = "Passwords do not match!";
        return false;
    }

    errorMessage.textContent = "";
    return true;
    
}