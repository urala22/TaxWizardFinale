document.addEventListener('DOMContentLoaded', function() {
    // Get all forms that need validation
    const forms = document.querySelectorAll('.needs-validation');
    
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Add custom validations for specific form inputs
    setupNumericValidation();
    setupEmailValidation();
    setupPasswordValidation();
    setupFileTypeValidation();
});

function setupNumericValidation() {
    // All inputs with data-type="numeric" should only accept numbers
    const numericInputs = document.querySelectorAll('input[data-type="numeric"]');
    
    numericInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            // Allow only numbers and decimal point
            this.value = this.value.replace(/[^0-9.]/g, '');
            
            // Ensure only one decimal point
            const parts = this.value.split('.');
            if (parts.length > 2) {
                this.value = parts[0] + '.' + parts.slice(1).join('');
            }
            
            // Check if number is negative when it shouldn't be
            if (parseFloat(this.value) < 0 && !this.hasAttribute('data-allow-negative')) {
                // Show validation error
                this.setCustomValidity('This value cannot be negative');
            } else {
                this.setCustomValidity('');
            }
        });
    });
}

function setupEmailValidation() {
    // Email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    
    emailInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            
            if (!emailRegex.test(this.value)) {
                this.setCustomValidity('Please enter a valid email address');
            } else {
                this.setCustomValidity('');
            }
        });
    });
}

function setupPasswordValidation() {
    // Password validation
    const passwordInputs = document.querySelectorAll('input[data-type="password-new"]');
    
    passwordInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            // Password must be at least 8 characters with at least one number, one uppercase letter, and one special character
            const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
            
            if (!passwordRegex.test(this.value)) {
                this.setCustomValidity('Password must be at least 8 characters with at least one lowercase letter, one uppercase letter, one number, and one special character');
            } else {
                this.setCustomValidity('');
            }
        });
    });
    
    // Password confirmation validation
    const passwordConfirms = document.querySelectorAll('input[data-type="password-confirm"]');
    
    passwordConfirms.forEach(input => {
        input.addEventListener('input', function(e) {
            const passwordInput = document.querySelector('input[data-type="password-new"]');
            
            if (this.value !== passwordInput.value) {
                this.setCustomValidity('Passwords do not match');
            } else {
                this.setCustomValidity('');
            }
        });
    });
}

function setupFileTypeValidation() {
    // File upload validation
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const allowedExtensions = this.getAttribute('data-allowed-extensions') || 'pdf,jpg,jpeg,png,csv,xls,xlsx,txt';
            const maxSize = parseInt(this.getAttribute('data-max-size') || '16') * 1024 * 1024; // Default to 16MB
            
            if (this.files.length > 0) {
                const file = this.files[0];
                const fileExtension = file.name.split('.').pop().toLowerCase();
                
                if (!allowedExtensions.split(',').includes(fileExtension)) {
                    this.setCustomValidity(`Invalid file type. Allowed types: ${allowedExtensions}`);
                } else if (file.size > maxSize) {
                    this.setCustomValidity(`File size too large. Maximum size: ${maxSize / (1024 * 1024)}MB`);
                } else {
                    this.setCustomValidity('');
                }
            }
        });
    });
}

// Function to update value display on a range input
function updateRangeValue(rangeId, valueId) {
    const range = document.getElementById(rangeId);
    const value = document.getElementById(valueId);
    
    if (range && value) {
        value.textContent = range.value;
        
        range.addEventListener('input', function() {
            value.textContent = this.value;
        });
    }
}
