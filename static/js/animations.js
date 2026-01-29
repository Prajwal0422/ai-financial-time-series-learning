/**
 * Professional Dashboard Animations & Interactions
 * Minimal, meaningful JS for a high-quality feel.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Staggered Entrance for KPI Cards
    const kpiCards = document.querySelectorAll('.kpi-card');
    kpiCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
            card.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
        }, 200 + (index * 150));
    });

    // 2. Enhanced Intersection Observer for Scroll Animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                
                // If it's the charts grid, stagger its children
                if (entry.target.classList.contains('charts-grid')) {
                    const charts = entry.target.querySelectorAll('.chart-card');
                    charts.forEach((chart, i) => {
                        setTimeout(() => {
                            chart.style.opacity = '1';
                            chart.style.transform = 'translateY(0)';
                            chart.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
                        }, i * 200);
                    });
                }

                // If it's the regime table
                if (entry.target.classList.contains('regime-table-container')) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    entry.target.style.transition = 'all 0.8s cubic-bezier(0.16, 1, 0.3, 1)';
                }

                // Panel items stagger animation
                if (entry.target.classList.contains('interpretation-panel')) {
                    const panelItems = entry.target.querySelectorAll('.panel-item');
                    panelItems.forEach((item, i) => {
                        setTimeout(() => {
                            item.style.opacity = '1';
                            item.style.transform = 'translateY(0)';
                            item.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
                        }, i * 250);
                    });
                }

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Register elements to observe
    document.querySelectorAll('.section-header, .charts-grid, .regime-table-container, .interpretation-panel').forEach(el => {
        revealObserver.observe(el);
    });

    // 3. Enhanced Dataset Selection Handler
    const datasetSelect = document.getElementById('dataset-select');
    if (datasetSelect) {
        datasetSelect.addEventListener('change', () => {
            const selectedDataset = datasetSelect.value;
            // Add a smooth fade out before redirecting
            document.body.style.opacity = '0';
            document.body.style.transition = 'opacity 0.4s ease';
            setTimeout(() => {
                window.location.href = `/dashboard?dataset=${selectedDataset}`;
            }, 400);
        });
    }

    // 4. Enhanced Image Loading with Smooth Fade-in
    const images = document.querySelectorAll('.chart-image');
    images.forEach(img => {
        // Add loading state
        img.parentElement.classList.add('loading');
        
        if (img.complete) {
            img.style.opacity = '1';
            img.parentElement.classList.remove('loading');
        } else {
            img.style.opacity = '0';
            img.style.transition = 'opacity 0.6s ease';
            img.onload = () => {
                img.style.opacity = '1';
                img.parentElement.classList.remove('loading');
            };
            img.onerror = () => {
                img.parentElement.classList.remove('loading');
                img.style.opacity = '0.3';
            };
        }
    });

    // 5. Subtle Hover Effects for Interactive Elements
    const interactiveElements = document.querySelectorAll('.kpi-card, .chart-card, .regime-badge');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            element.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });

    // 6. Smooth Scroll for Internal Links (if any)
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

    // 7. Performance Optimization: Throttle scroll events
    let ticking = false;
    function updateAnimations() {
        if (!ticking) {
            requestAnimationFrame(() => {
                // Update any scroll-based animations here
                ticking = false;
            });
            ticking = true;
        }
    }
    window.addEventListener('scroll', updateAnimations, { passive: true });

    // 8. Add subtle parallax effect to hero header
    const heroHeader = document.querySelector('.hero-header');
    if (heroHeader) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const parallax = scrolled * 0.5;
            heroHeader.style.transform = `translateY(${parallax}px)`;
            heroHeader.style.opacity = 1 - scrolled / 600;
        }, { passive: true });
    }

    // 9. Initialize panel items with hidden state
    const panelItems = document.querySelectorAll('.panel-item');
    panelItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(30px)';
    });

    // 10. Add keyboard navigation support
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && datasetSelect) {
            datasetSelect.blur();
        }
    });

    console.log('Dashboard animations initialized successfully');
});
