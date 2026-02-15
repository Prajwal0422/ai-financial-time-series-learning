// Professional Analytics Platform - UI Effects
// Minimal, purposeful animations for enterprise interface

(function() {
    'use strict';

    // Fade-in on scroll observer
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const fadeInObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                fadeInObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements that should fade in
    document.addEventListener('DOMContentLoaded', () => {
        const fadeElements = document.querySelectorAll(
            '.feature-card, .chart-card, .metric-card, .info-panel'
        );
        
        fadeElements.forEach(el => {
            fadeInObserver.observe(el);
        });

        // Dataset selector change handler
        const datasetSelect = document.getElementById('dataset-select');
        if (datasetSelect) {
            datasetSelect.addEventListener('change', function() {
                window.location.href = `/dashboard?dataset=${this.value}`;
            });
        }

        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
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
    });

    // Performance monitoring (optional)
    if (window.performance && window.performance.timing) {
        window.addEventListener('load', () => {
            const loadTime = window.performance.timing.domContentLoadedEventEnd - 
                           window.performance.timing.navigationStart;
            console.log(`Page loaded in ${loadTime}ms`);
        });
    }
})();
