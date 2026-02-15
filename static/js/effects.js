// Premium Dark Analytics Platform - Effects & Interactions

(function() {
    'use strict';

    // Intersection Observer for scroll animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                scrollObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Initialize on DOM load
    document.addEventListener('DOMContentLoaded', () => {
        // Observe elements for scroll animation
        const animateElements = document.querySelectorAll(
            '.glass-card, .surface-card, .metric-card, .chart-card, .feature-card'
        );
        
        animateElements.forEach(el => {
            scrollObserver.observe(el);
        });

        // Dataset selector
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

        // Parallax effect for hero (subtle)
        const hero = document.querySelector('.hero');
        if (hero) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const parallax = scrolled * 0.3;
                hero.style.transform = `translateY(${parallax}px)`;
            });
        }

        // Add glow effect to cards on mouse move
        const glowCards = document.querySelectorAll('.surface-card, .glass-card');
        glowCards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
            });
        });

        // Table row hover effect
        const tableRows = document.querySelectorAll('.data-table tbody tr');
        tableRows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.background = 'rgba(6, 182, 212, 0.05)';
            });
            row.addEventListener('mouseleave', function() {
                this.style.background = '';
            });
        });

        // Performance monitoring
        if (window.performance && window.performance.timing) {
            window.addEventListener('load', () => {
                const loadTime = window.performance.timing.domContentLoadedEventEnd - 
                               window.performance.timing.navigationStart;
                console.log(`Dashboard loaded in ${loadTime}ms`);
            });
        }
    });

    // Add subtle cursor glow effect
    const cursor = document.createElement('div');
    cursor.className = 'cursor-glow';
    cursor.style.cssText = `
        position: fixed;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.3), transparent);
        pointer-events: none;
        z-index: 9999;
        transition: transform 0.2s ease;
        display: none;
    `;
    document.body.appendChild(cursor);

    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX - 10 + 'px';
        cursor.style.top = e.clientY - 10 + 'px';
        cursor.style.display = 'block';
    });

})();
