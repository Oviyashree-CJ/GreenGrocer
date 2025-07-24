// GreenGrocer Grocery Store - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeCartActions();
    initializeFormValidation();
    initializeImageLazyLoading();
    initializeTooltips();
    initializeQuantityControls();
    initializePaymentOptions();
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);
});

// Cart functionality
function initializeCartActions() {
    const addToCartButtons = document.querySelectorAll('a[href*="add_to_cart"]');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Add loading state
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="loading"></span> Adding...';
            this.classList.add('disabled');
            
            // Simulate network delay for better UX
            setTimeout(() => {
                window.location.href = this.href;
            }, 500);
        });
    });
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            this.classList.add('was-validated');
        });
    });
    
    // Password validation for registration
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    
    if (passwordInput) {
        passwordInput.addEventListener('input', validatePassword);
    }
    
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', function() {
            if (this.value !== passwordInput.value) {
                this.setCustomValidity('Passwords do not match');
            } else {
                this.setCustomValidity('');
            }
        });
    }
}

// Password validation function
function validatePassword() {
    const password = this.value;
    const digitCount = (password.match(/\d/g) || []).length;
    const hasSpecialChars = /[^a-zA-Z0-9]/.test(password);
    
    if (password.length < 4) {
        this.setCustomValidity('Password must be at least 4 characters long');
    } else if (digitCount !== 2) {
        this.setCustomValidity('Password must contain exactly 2 numbers');
    } else if (hasSpecialChars) {
        this.setCustomValidity('Password cannot contain special characters');
    } else {
        this.setCustomValidity('');
    }
}

// Lazy loading for images
function initializeImageLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Quantity controls
function initializeQuantityControls() {
    const quantityInputs = document.querySelectorAll('input[type="number"][name="quantity"]');
    
    quantityInputs.forEach(input => {
        const minValue = parseInt(input.min) || 0;
        const maxValue = parseInt(input.max) || 99;
        
        input.addEventListener('input', function() {
            let value = parseInt(this.value);
            
            if (isNaN(value) || value < minValue) {
                this.value = minValue;
            } else if (value > maxValue) {
                this.value = maxValue;
            }
        });
        
        // Add increment/decrement buttons
        const wrapper = document.createElement('div');
        wrapper.className = 'input-group input-group-sm';
        
        const decrementBtn = document.createElement('button');
        decrementBtn.className = 'btn btn-outline-secondary';
        decrementBtn.type = 'button';
        decrementBtn.innerHTML = '<i class="fas fa-minus"></i>';
        decrementBtn.addEventListener('click', () => {
            const currentValue = parseInt(input.value) || 0;
            if (currentValue > minValue) {
                input.value = currentValue - 1;
                input.dispatchEvent(new Event('input'));
            }
        });
        
        const incrementBtn = document.createElement('button');
        incrementBtn.className = 'btn btn-outline-secondary';
        incrementBtn.type = 'button';
        incrementBtn.innerHTML = '<i class="fas fa-plus"></i>';
        incrementBtn.addEventListener('click', () => {
            const currentValue = parseInt(input.value) || 0;
            if (currentValue < maxValue) {
                input.value = currentValue + 1;
                input.dispatchEvent(new Event('input'));
            }
        });
        
        // Only add buttons if input is not in a form that has its own buttons
        if (!input.closest('.input-group')) {
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(decrementBtn);
            wrapper.appendChild(input);
            wrapper.appendChild(incrementBtn);
        }
    });
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertContainer, container.firstChild);
    }
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertContainer);
        bsAlert.close();
    }, 5000);
}

function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Search functionality (if needed)
function initializeSearch() {
    const searchInput = document.getElementById('search');
    if (searchInput) {
        const debouncedSearch = debounce((query) => {
            // Implement search functionality
            console.log('Searching for:', query);
        }, 300);
        
        searchInput.addEventListener('input', (e) => {
            debouncedSearch(e.target.value);
        });
    }
}

// Payment options functionality
function initializePaymentOptions() {
    const codRadio = document.getElementById('cod');
    const onlineRadio = document.getElementById('online');
    const onlinePaymentOptions = document.getElementById('onlinePaymentOptions');
    const paymentPasswordSection = document.getElementById('paymentPasswordSection');
    const paymentAppButtons = document.querySelectorAll('.payment-app-btn');
    const selectedPaymentApp = document.getElementById('selectedPaymentApp');
    const paymentForm = document.querySelector('form');
    
    if (!codRadio || !onlineRadio) return;
    
    // Show/hide online payment options
    function toggleOnlineOptions() {
        if (onlineRadio.checked) {
            onlinePaymentOptions.style.display = 'block';
        } else {
            onlinePaymentOptions.style.display = 'none';
            paymentPasswordSection.style.display = 'none';
        }
    }
    
    codRadio.addEventListener('change', toggleOnlineOptions);
    onlineRadio.addEventListener('change', toggleOnlineOptions);
    
    // Handle payment app selection
    paymentAppButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active state from all buttons
            paymentAppButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active state to clicked button
            this.classList.add('active');
            
            // Show password section
            paymentPasswordSection.style.display = 'block';
            selectedPaymentApp.textContent = this.dataset.app;
            
            // Update form payment method value
            onlineRadio.value = `Online Payment - ${this.dataset.app}`;
        });
    });
    
    // Form submission handling
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            if (onlineRadio.checked) {
                const passwordInput = document.getElementById('payment_password');
                const selectedApp = document.querySelector('.payment-app-btn.active');
                
                if (!selectedApp) {
                    e.preventDefault();
                    showAlert('Please select a payment app (Paytm, PhonePe, or GPay)', 'warning');
                    return;
                }
                
                if (!passwordInput.value.trim()) {
                    e.preventDefault();
                    showAlert('Please enter your payment password', 'warning');
                    passwordInput.focus();
                    return;
                }
                
                // Simulate payment processing
                e.preventDefault();
                const submitButton = this.querySelector('button[type="submit"]');
                const originalText = submitButton.innerHTML;
                
                submitButton.innerHTML = '<span class="loading"></span> Processing Payment...';
                submitButton.disabled = true;
                
                setTimeout(() => {
                    // Show success message
                    showAlert('Your order is placed successfully!', 'success');
                    
                    // Submit the form after showing success message
                    setTimeout(() => {
                        this.submit();
                    }, 1500);
                }, 2000);
            }
        });
    }
}

// Export functions for external use
window.FreshMart = {
    showAlert,
    formatPrice,
    debounce
};
