/**
 * Modern UI Enhancements
 * Professional animations, interactions, and visual effects
 */

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function() {
    initParticles();
    initCounters();
    initGauges();
    initScrollAnimations();
    initNavbar();
});

/**
 * Create floating particles background
 */
function initParticles() {
    const particlesContainer = document.querySelector('.particles');
    if (!particlesContainer) return;
    
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random position
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        
        // Random animation delay and duration
        particle.style.animationDelay = Math.random() * 20 + 's';
        particle.style.animationDuration = (15 + Math.random() * 10) + 's';
        
        particlesContainer.appendChild(particle);
    }
}

/**
 * Animated number counters
 */
function initCounters() {
    const counters = document.querySelectorAll('.stat-value, .metric-value-large, .gauge-value');
    
    counters.forEach(counter => {
        const target = parseFloat(counter.textContent.replace(/[^0-9.]/g, ''));
        if (isNaN(target)) return;
        
        const duration = 2000; // 2 seconds
        const steps = 60;
        const increment = target / steps;
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            // Format based on original content
            if (counter.textContent.includes('%')) {
                counter.textContent = current.toFixed(1) + '%';
            } else if (counter.textContent.includes(',')) {
                counter.textContent = Math.round(current).toLocaleString();
            } else if (target < 10) {
                counter.textContent = current.toFixed(4);
            } else {
                counter.textContent = Math.round(current);
            }
        }, duration / steps);
    });
}

/**
 * Initialize circular gauges
 */
function initGauges() {
    const gauges = document.querySelectorAll('.gauge-progress');
    
    gauges.forEach(gauge => {
        const percentage = parseFloat(gauge.getAttribute('data-percentage') || 0);
        const radius = parseFloat(gauge.getAttribute('r'));
        const circumference = 2 * Math.PI * radius;
        
        gauge.style.strokeDasharray = circumference;
        gauge.style.strokeDashoffset = circumference;
        
        // Animate
        setTimeout(() => {
            const offset = circumference - (percentage / 100) * circumference;
            gauge.style.strokeDashoffset = offset;
        }, 500);
    });
}

/**
 * Progress bars animation
 */
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const width = bar.getAttribute('data-width') || '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 300);
    });
}

/**
 * Scroll-triggered animations
 */
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements
    document.querySelectorAll('.stat-card, .feature-card, .metric-item, .chart-card').forEach(el => {
        observer.observe(el);
    });
    
    // Animate progress bars when visible
    const progressObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateProgressBars();
                progressObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.progress-bar-container').forEach(el => {
        progressObserver.observe(el);
    });
}

/**
 * Enhanced navbar with scroll effects
 */
function initNavbar() {
    const header = document.querySelector('.header');
    if (!header) return;
    
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });
    
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const headerNav = document.querySelector('.header-nav');
    
    if (mobileMenuBtn && headerNav) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenuBtn.classList.toggle('active');
            headerNav.classList.toggle('active');
        });
    }
}

/**
 * Smooth scroll to anchors
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

/**
 * Copy to clipboard functionality
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

/**
 * Show notification toast
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#10b981' : '#06b6d4'};
        color: white;
        border-radius: 0.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Format large numbers
 */
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

/**
 * Format percentage
 */
function formatPercentage(num, decimals = 2) {
    return (num * 100).toFixed(decimals) + '%';
}

/**
 * Debounce function for performance
 */
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

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
