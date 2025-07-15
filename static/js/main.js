// Main JavaScript file for Innovator Match
document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Password confirmation validation
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    
    if (passwordField && confirmPasswordField) {
        function validatePassword() {
            if (passwordField.value !== confirmPasswordField.value) {
                confirmPasswordField.setCustomValidity('Passwords do not match');
            } else {
                confirmPasswordField.setCustomValidity('');
            }
        }
        
        passwordField.addEventListener('input', validatePassword);
        confirmPasswordField.addEventListener('input', validatePassword);
    }
    
    // Search functionality with debounce
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.trim() !== '') {
                    // Auto-submit search form after 500ms of no typing
                    this.form.submit();
                }
            }, 500);
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add loading state to buttons on form submission
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.classList.add('loading');
                submitButton.disabled = true;
                
                // Re-enable button after 3 seconds (fallback)
                setTimeout(() => {
                    submitButton.classList.remove('loading');
                    submitButton.disabled = false;
                }, 3000);
            }
        });
    });
    
    // Character counter for textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            const counter = document.createElement('small');
            counter.className = 'form-text text-muted';
            counter.style.float = 'right';
            
            function updateCounter() {
                const remaining = maxLength - textarea.value.length;
                counter.textContent = `${remaining} characters remaining`;
                
                if (remaining < 20) {
                    counter.classList.add('text-warning');
                } else {
                    counter.classList.remove('text-warning');
                }
            }
            
            textarea.addEventListener('input', updateCounter);
            textarea.parentNode.insertBefore(counter, textarea.nextSibling);
            updateCounter();
        }
    });
    
    // Tooltip initialization
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Popover initialization
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Handle mobile menu
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking a link
        navbarCollapse.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                    toggle: false
                });
                bsCollapse.hide();
            });
        });
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Alt + D for Dashboard
        if (e.altKey && e.key === 'd') {
            e.preventDefault();
            const dashboardLink = document.querySelector('a[href*="dashboard"]');
            if (dashboardLink) dashboardLink.click();
        }
        
        // Alt + P for Profile
        if (e.altKey && e.key === 'p') {
            e.preventDefault();
            const profileLink = document.querySelector('a[href*="profile"]');
            if (profileLink) profileLink.click();
        }
        
        // Alt + N for Notifications
        if (e.altKey && e.key === 'n') {
            e.preventDefault();
            const notificationsLink = document.querySelector('a[href*="notifications"]');
            if (notificationsLink) notificationsLink.click();
        }
        
        // Alt + C for Chat
        if (e.altKey && e.key === 'c') {
            e.preventDefault();
            const chatLink = document.querySelector('a[href*="chat"]');
            if (chatLink) chatLink.click();
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const activeModal = document.querySelector('.modal.show');
            if (activeModal) {
                const bsModal = bootstrap.Modal.getInstance(activeModal);
                if (bsModal) bsModal.hide();
            }
        }
    });
    
    // Auto-focus first input field
    const firstInput = document.querySelector('input[type="text"], input[type="email"], textarea');
    if (firstInput && !firstInput.hasAttribute('readonly')) {
        firstInput.focus();
    }
    
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.innovator-card, .notification-card, .profile-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
    
    // Handle enter key in chat input
    const chatInput = document.getElementById('messageInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const form = this.closest('form');
                if (form) {
                    form.dispatchEvent(new Event('submit'));
                }
            }
        });
    }
    
    // Update page title with unread count (placeholder for future implementation)
    function updatePageTitle(unreadCount = 0) {
        const baseTitle = 'Thynkly';
        if (unreadCount > 0) {
            document.title = `(${unreadCount}) ${baseTitle}`;
        } else {
            document.title = baseTitle;
        }
    }
    
    // Initialize page
    updatePageTitle();
    
    console.log('Thynkly initialized successfully!');
});

// Utility functions
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) {
        return 'Just now';
    } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else {
        return date.toLocaleDateString();
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy to clipboard', 'error');
    });
}
