/**
 * UI Effects - Professional Analytics Platform
 * Minimal, purposeful animations for analytical clarity
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all UI effects
    initializeAnimations();
    initializeInteractions();
    initializeScrollEffects();
    
    console.log('Professional analytics platform UI effects initialized');
});

/**
 * Initialize page load animations
 */
function initializeAnimations() {
    // Hero section animations
    animateHeroSection();
    
    // Feature cards staggered animation
    animateFeatureCards();
    
    // Dashboard elements
    animateDashboardElements();
}

/**
 * Initialize interactive elements
 */
function initializeInteractions() {
    // Button hover effects
    setupButtonEffects();
    
    // Card hover effects
    setupCardEffects();
    
    // Dataset selector
    setupDatasetSelector();
}

/**
 * Initialize scroll-based animations
 */
function initializeScrollEffects() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements for scroll animations
    const scrollElements = document.querySelectorAll('.feature-card, .chart-card, .interpretation-item, .info-panel');
    scrollElements.forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
}

/**
 * Animate hero section elements
 */
function animateHeroSection() {
    const heroTitle = document.querySelector('.hero h1');
    const heroSubtitle = document.querySelector('.hero .subtitle');
    const heroDescription = document.querySelector('.hero .description');
    const heroCta = document.querySelector('.hero-cta');
    
    if (heroTitle) {
        heroTitle.style.opacity = '0';
        heroTitle.classList.add('animate-slide-down');
        setTimeout(() => {
            heroTitle.style.opacity = '1';
        }, 100);
    }
    
    if (heroSubtitle) {
        heroSubtitle.style.opacity = '0';
        heroSubtitle.classList.add('animate-fade-in');
        setTimeout(() => {
            heroSubtitle.style.opacity = '1';
        }, 300);
    }
    
    if (heroDescription) {
        heroDescription.style.opacity = '0';
        heroDescription.classList.add('animate-fade-in');
        setTimeout(() => {
            heroDescription.style.opacity = '1';
        }, 500);
    }
    
    if (heroCta) {
        heroCta.style.opacity = '0';
        heroCta.classList.add('animate-slide-up');
        setTimeout(() => {
            heroCta.style.opacity = '1';
        }, 700);
    }
}

/**
 * Animate feature cards with stagger
 */
function animateFeatureCards() {
    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 200 * (index + 1));
    });
}

/**
 * Animate dashboard elements
 */
function animateDashboardElements() {
    // KPI cards staggered animation
    const kpiCards = document.querySelectorAll('.metric-card');
    
    kpiCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * (index + 1));
    });
    
    // Chart cards animation
    const chartCards = document.querySelectorAll('.chart-card');
    
    chartCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 300 + (100 * index));
    });
}

/**
 * Setup button hover effects
 */
function setupButtonEffects() {
    const buttons = document.querySelectorAll('.button-primary, .button-secondary');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.2s ease';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transition = 'all 0.2s ease';
        });
    });
}

/**
 * Setup card hover effects
 */
function setupCardEffects() {
    const cards = document.querySelectorAll('.metric-card, .chart-card, .info-panel');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.2s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transition = 'all 0.2s ease';
        });
    });
}

/**
 * Setup dataset selector functionality
 */
function setupDatasetSelector() {
    const selector = document.getElementById('dataset-select');
    
    if (selector) {
        selector.addEventListener('change', function() {
            const selectedDataset = this.value;
            const currentUrl = new URL(window.location);
            currentUrl.searchParams.set('dataset', selectedDataset);
            window.location.href = currentUrl.toString();
        });
    }
}

/**
 * Smooth scroll for anchor links
 */
function setupSmoothScroll() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Add loading states for images
 */
function setupImageLoading() {
    const images = document.querySelectorAll('.chart-container img');
    
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '0';
            this.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                this.style.opacity = '1';
            }, 100);
        });
        
        img.addEventListener('error', function() {
            this.style.display = 'none';
            const container = this.closest('.chart-container');
            if (container) {
                container.innerHTML = '<div style="color: var(--color-text-muted); text-align: center; padding: 2rem;">Chart image not available</div>';
            }
        });
    });
}

/**
 * Performance monitoring
 */
function trackPerformance() {
    // Track page load time
    window.addEventListener('load', function() {
        const loadTime = performance.now();
        console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
    });
    
    // Track interaction performance
    let interactionStart = 0;
    
    document.addEventListener('click', function() {
        interactionStart = performance.now();
    });
    
    document.addEventListener('clickend', function() {
        if (interactionStart > 0) {
            const interactionTime = performance.now() - interactionStart;
            console.log(`Interaction took ${interactionTime.toFixed(2)}ms`);
            interactionStart = 0;
        }
    });
}

// Initialize performance tracking
trackPerformance();

// Export functions for potential external use
window.AnalyticsUI = {
    animateHeroSection,
    animateFeatureCards,
    animateDashboardElements,
    setupSmoothScroll
};
