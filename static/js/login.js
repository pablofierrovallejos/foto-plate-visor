// Login Page JavaScript

// Handle Google Sign-In Response
function handleCredentialResponse(response) {
    // Send the credential to your backend
    fetch('/auth/google', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            credential: response.credential
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirect to dashboard or home page
            window.location.href = data.redirect_url || '/';
        } else {
            // Show error message
            showAlert('Error al iniciar sesión con Google: ' + data.message, 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error de conexión. Intenta nuevamente.', 'danger');
    });
}

// Show alert messages
function showAlert(message, type) {
    const alertContainer = document.querySelector('.login-card-body');
    const existingAlert = alertContainer.querySelector('.alert');
    
    if (existingAlert) {
        existingAlert.remove();
    }
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.role = 'alert';
    alert.innerHTML = `
        ${message}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    `;
    
    alertContainer.insertBefore(alert, alertContainer.firstChild);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

// Handle traditional form submission
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('form[method="POST"]');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(loginForm);
            const data = Object.fromEntries(formData);
            
            fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = data.redirect_url || '/';
                } else {
                    showAlert(data.message || 'Error al iniciar sesión', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error de conexión. Intenta nuevamente.', 'danger');
            });
        });
    }
    
    // Add loading states to buttons
    const submitBtn = document.querySelector('.login-submit-btn');
    if (submitBtn) {
        submitBtn.addEventListener('click', function() {
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Iniciando sesión...';
            this.disabled = true;
        });
    }
});

// Initialize Google Sign-In when page loads
window.addEventListener('load', function() {
    // Google Sign-In will initialize automatically with the data attributes
    console.log('Google Sign-In initialized');
});
