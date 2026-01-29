/**
 * Superb Dashboard Animations & Interactions
 * Enhanced with impressive effects and smooth transitions
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Spectacular Entrance for KPI Cards
    const kpiCards = document.querySelectorAll('.kpi-card');
    kpiCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0) scale(1)';
            card.style.transition = 'all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)';
            
            // Add a pulse effect after entrance
            setTimeout(() => {
                card.style.transform = 'translateY(0) scale(1.05)';
                setTimeout(() => {
                    card.style.transform = 'translateY(0) scale(1)';
                }, 200);
            }, 300);
        }, 300 + (index * 200));
    });

    // 2. Enhanced Intersection Observer with Dramatic Effects
    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -100px 0px'
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                
                // Charts grid with spectacular entrance
                if (entry.target.classList.contains('charts-grid')) {
                    const charts = entry.target.querySelectorAll('.chart-card');
                    charts.forEach((chart, i) => {
                        setTimeout(() => {
                            chart.style.opacity = '1';
                            chart.style.transform = 'translateY(0) scale(1)';
                            chart.style.transition = 'all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)';
                            
                            // Add rotation effect
                            setTimeout(() => {
                                chart.style.transform = 'translateY(0) scale(1.02) rotateZ(1deg)';
                                setTimeout(() => {
                                    chart.style.transform = 'translateY(0) scale(1) rotateZ(0deg)';
                                }, 300);
                            }, 400);
                        }, i * 250);
                    });
                }

                // Regime table with slide-in effect
                if (entry.target.classList.contains('regime-table-container')) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0) scale(1)';
                    entry.target.style.transition = 'all 1s cubic-bezier(0.34, 1.56, 0.64, 1)';
                }

                // Panel items with staggered entrance
                if (entry.target.classList.contains('interpretation-panel')) {
                    const panelItems = entry.target.querySelectorAll('.panel-item');
                    panelItems.forEach((item, i) => {
                        setTimeout(() => {
                            item.style.opacity = '1';
                            item.style.transform = 'translateY(0) scale(1)';
                            item.style.transition = 'all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)';
                        }, i * 300);
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

    // 3. Enhanced Dataset Selection with Morphing Effect
    const datasetSelect = document.getElementById('dataset-select');
    if (datasetSelect) {
        datasetSelect.addEventListener('change', () => {
            const selectedDataset = datasetSelect.value;
            
            // Create a spectacular morphing effect
            document.body.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            document.body.style.transform = 'scale(0.95)';
            document.body.style.opacity = '0';
            document.body.style.filter = 'blur(10px)';
            
            setTimeout(() => {
                window.location.href = `/dashboard?dataset=${selectedDataset}`;
            }, 600);
        });
    }

    // 4. Enhanced Image Loading with Spectacular Effects
    const images = document.querySelectorAll('.chart-image');
    images.forEach(img => {
        // Add loading state with shimmer
        img.parentElement.classList.add('loading');
        
        if (img.complete) {
            img.style.opacity = '1';
            img.style.transform = 'scale(1)';
            img.parentElement.classList.remove('loading');
        } else {
            img.style.opacity = '0';
            img.style.transform = 'scale(0.8)';
            img.style.transition = 'all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)';
            
            img.onload = () => {
                img.style.opacity = '1';
                img.style.transform = 'scale(1)';
                img.parentElement.classList.remove('loading');
                
                // Add a subtle zoom effect after load
                setTimeout(() => {
                    img.style.transform = 'scale(1.05)';
                    setTimeout(() => {
                        img.style.transform = 'scale(1)';
                    }, 300);
                }, 200);
            };
            
            img.onerror = () => {
                img.parentElement.classList.remove('loading');
                img.style.opacity = '0.3';
                img.style.transform = 'scale(1)';
            };
        }
    });

    // 5. Magnificent Hover Effects
    const interactiveElements = document.querySelectorAll('.kpi-card, .chart-card, .regime-badge');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            element.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            
            // Add a subtle glow effect
            if (element.classList.contains('kpi-card') || element.classList.contains('chart-card')) {
                element.style.boxShadow = '0 25px 50px -12px rgba(102, 126, 234, 0.4)';
            }
        });
        
        element.addEventListener('mouseleave', () => {
            if (element.classList.contains('kpi-card') || element.classList.contains('chart-card')) {
                element.style.boxShadow = '';
            }
        });
    });

    // 6. Smooth Scroll with Parallax Enhancement
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

    // 7. Advanced Performance Optimization
    let ticking = false;
    function updateAnimations() {
        if (!ticking) {
            requestAnimationFrame(() => {
                // Update scroll-based animations
                const scrolled = window.pageYOffset;
                const parallaxElements = document.querySelectorAll('.hero-header');
                
                parallaxElements.forEach(element => {
                    const speed = 0.5;
                    const yPos = -(scrolled * speed);
                    element.style.transform = `translateY(${yPos}px)`;
                    element.style.opacity = 1 - (scrolled / 800);
                });
                
                ticking = false;
            });
            ticking = true;
        }
    }
    window.addEventListener('scroll', updateAnimations, { passive: true });

    // 8. Dynamic Background Particles Effect
    function createParticle() {
        const particle = document.createElement('div');
        particle.style.position = 'fixed';
        particle.style.width = '4px';
        particle.style.height = '4px';
        particle.style.background = 'rgba(255, 255, 255, 0.6)';
        particle.style.borderRadius = '50%';
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '1';
        particle.style.left = Math.random() * window.innerWidth + 'px';
        particle.style.top = window.innerHeight + 'px';
        
        document.body.appendChild(particle);
        
        const duration = 3000 + Math.random() * 2000;
        const horizontalMovement = (Math.random() - 0.5) * 100;
        
        particle.animate([
            { transform: 'translateY(0) translateX(0) scale(1)', opacity: 0 },
            { transform: 'translateY(-100px) translateX(0) scale(1)', opacity: 1 },
            { transform: `translateY(-${window.innerHeight + 100}px) translateX(${horizontalMovement}px) scale(0.5)`, opacity: 0 }
        ], {
            duration: duration,
            easing: 'ease-out'
        }).onfinish = () => particle.remove();
    }
    
    // Create particles periodically
    setInterval(createParticle, 500);

    // 9. Initialize Panel Items with Hidden State
    const panelItems = document.querySelectorAll('.panel-item');
    panelItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(50px) scale(0.9)';
    });

    // 10. Enhanced Keyboard Navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && datasetSelect) {
            datasetSelect.blur();
        }
        
        // Add keyboard shortcuts for navigation
        if (e.key === 'ArrowDown' && e.ctrlKey) {
            window.scrollBy({ top: 200, behavior: 'smooth' });
        }
        if (e.key === 'ArrowUp' && e.ctrlKey) {
            window.scrollBy({ top: -200, behavior: 'smooth' });
        }
    });

    // 11. Add Loading Animation to Page
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.8s ease-out';
        document.body.style.opacity = '1';
    }, 100);

    console.log('✨ Superb dashboard animations initialized successfully!');
});
