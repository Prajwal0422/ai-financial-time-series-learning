// Premium Dark Analytics Platform - Effects & Interactions

(function() {
    'use strict';

    // Navbar scroll effect
    let lastScroll = 0;
    const header = document.querySelector('.header');
    const navProgress = document.createElement('div');
    navProgress.className = 'nav-progress';
    if (header) {
        header.appendChild(navProgress);
    }

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        // Add scrolled class for background effect
        if (currentScroll > 50) {
            header?.classList.add('scrolled');
        } else {
            header?.classList.remove('scrolled');
        }

        // Update progress bar
        const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (currentScroll / windowHeight) * 100;
        if (navProgress) {
            navProgress.style.width = scrolled + '%';
        }

        lastScroll = currentScroll;
    });

    // Active nav link highlighting
    function setActiveNavLink() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.header-nav a');
        
        navLinks.forEach(link => {
            const linkPath = new URL(link.href).pathname;
            if (linkPath === currentPath) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

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
        // Set active nav link
        setActiveNavLink();

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
                // Add loading state
                this.style.opacity = '0.6';
                this.style.pointerEvents = 'none';
                
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

        // Enhanced card hover effects with mouse tracking
        const glowCards = document.querySelectorAll('.surface-card, .glass-card');
        glowCards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                // Create spotlight effect
                const spotlight = `radial-gradient(circle at ${x}px ${y}px, rgba(6, 182, 212, 0.1), transparent 50%)`;
                card.style.background = `${spotlight}, ${getComputedStyle(card).background}`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.background = '';
            });
        });

        // Table row hover effect with smooth transitions
        const tableRows = document.querySelectorAll('.data-table tbody tr');
        tableRows.forEach((row, index) => {
            // Stagger animation on load
            row.style.animation = `fadeIn 0.5s ease-out ${index * 0.05}s both`;
            
            row.addEventListener('mouseenter', function() {
                this.style.background = 'rgba(6, 182, 212, 0.05)';
                this.style.transform = 'translateX(4px)';
            });
            row.addEventListener('mouseleave', function() {
                this.style.background = '';
                this.style.transform = '';
            });
        });

        // Metric cards counter animation
        const metricValues = document.querySelectorAll('.metric-value');
        metricValues.forEach(metric => {
            const text = metric.textContent;
            const number = parseFloat(text.replace(/[^0-9.-]/g, ''));
            
            if (!isNaN(number) && number > 0) {
                animateCounter(metric, 0, number, 1500, text);
            }
        });

        // Chart image lazy loading with fade-in
        const chartImages = document.querySelectorAll('.chart-container img');
        chartImages.forEach(img => {
            img.style.opacity = '0';
            img.style.transition = 'opacity 0.6s ease';
            
            img.addEventListener('load', function() {
                this.style.opacity = '1';
            });
        });

        // Performance monitoring
        if (window.performance && window.performance.timing) {
            window.addEventListener('load', () => {
                const loadTime = window.performance.timing.domContentLoadedEventEnd - 
                               window.performance.timing.navigationStart;
                console.log(`✓ Dashboard loaded in ${loadTime}ms`);
            });
        }

        // Add keyboard navigation for nav links
        const navLinks = document.querySelectorAll('.header-nav a');
        navLinks.forEach((link, index) => {
            link.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowRight' && navLinks[index + 1]) {
                    navLinks[index + 1].focus();
                } else if (e.key === 'ArrowLeft' && navLinks[index - 1]) {
                    navLinks[index - 1].focus();
                }
            });
        });
    });

    // Counter animation function
    function animateCounter(element, start, end, duration, originalText) {
        const startTime = performance.now();
        const prefix = originalText.replace(/[0-9.-]/g, '').trim();
        
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const current = start + (end - start) * easeOutQuart;
            
            element.textContent = prefix + current.toFixed(2);
            
            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                element.textContent = originalText;
            }
        }
        
        requestAnimationFrame(update);
    }

    // Add subtle cursor glow effect
    const cursor = document.createElement('div');
    cursor.className = 'cursor-glow';
    cursor.style.cssText = `
        position: fixed;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.4), transparent 70%);
        pointer-events: none;
        z-index: 9999;
        transition: transform 0.15s ease, opacity 0.15s ease;
        opacity: 0;
        mix-blend-mode: screen;
    `;
    document.body.appendChild(cursor);

    let cursorX = 0, cursorY = 0;
    let cursorVisible = false;

    document.addEventListener('mousemove', (e) => {
        cursorX = e.clientX;
        cursorY = e.clientY;
        
        if (!cursorVisible) {
            cursor.style.opacity = '1';
            cursorVisible = true;
        }
        
        cursor.style.left = (cursorX - 12) + 'px';
        cursor.style.top = (cursorY - 12) + 'px';
    });

    document.addEventListener('mouseleave', () => {
        cursor.style.opacity = '0';
        cursorVisible = false;
    });

    // Scale cursor on interactive elements
    const interactiveElements = document.querySelectorAll('a, button, .selector, .data-table tr');
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursor.style.transform = 'scale(1.5)';
        });
        el.addEventListener('mouseleave', () => {
            cursor.style.transform = 'scale(1)';
        });
    });

})();
