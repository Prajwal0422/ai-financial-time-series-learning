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
        }, 100 + (index * 100));
    });

    // 2. Intersection Observer for Scroll Animations
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
                        }, i * 150);
                    });
                }

                // If it's the regime table
                if (entry.target.classList.contains('regime-table-container')) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    entry.target.style.transition = 'all 0.8s ease-out';
                }

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Register elements to observe
    document.querySelectorAll('.section-header, .charts-grid, .regime-table-container, .panel-item').forEach(el => {
        revealObserver.observe(el);
    });

    // 3. Dataset Selection Handler
    const datasetSelect = document.getElementById('dataset-select');
    if (datasetSelect) {
        datasetSelect.addEventListener('change', () => {
            const selectedDataset = datasetSelect.value;
            // Add a slight fade out before redirecting
            document.body.style.opacity = '0.5';
            document.body.style.transition = 'opacity 0.3s ease';
            window.location.href = `/dashboard?dataset=${selectedDataset}`;
        });
    }

    // 4. Handle Image Loading (Smooth Fade-in)
    const images = document.querySelectorAll('.chart-image');
    images.forEach(img => {
        if (img.complete) {
            img.style.opacity = '1';
        } else {
            img.style.opacity = '0';
            img.style.transition = 'opacity 0.5s ease';
            img.onload = () => img.style.opacity = '1';
        }
    });
});
