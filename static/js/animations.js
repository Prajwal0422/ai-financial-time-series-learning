/**
 * Professional Dashboard Animations
 * Minimal, purposeful animations for analytical clarity
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Animate KPI cards on page load
    function animateKPICards() {
        const kpiCards = document.querySelectorAll('.kpi-card');
        kpiCards.forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
                card.style.transition = 'all 0.6s ease-out';
            }, 100 * (index + 1));
        });
    }
    
    // Animate chart cards when they come into view
    function animateChartsOnScroll() {
        const chartCards = document.querySelectorAll('.chart-card');
        const interpretationItems = document.querySelectorAll('.interpretation-item');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    entry.target.style.transition = 'all 0.6s ease-out';
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        chartCards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            observer.observe(card);
        });
        
        interpretationItems.forEach(item => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            observer.observe(item);
        });
    }
    
    // Handle dataset selection
    function handleDatasetSelection() {
        const selector = document.getElementById('dataset-select');
        if (selector) {
            selector.addEventListener('change', function() {
                const selectedDataset = this.value;
                window.location.href = `/dashboard?dataset=${selectedDataset}`;
            });
        }
    }
    
    // Initialize all animations
    function init() {
        // Start KPI animation after a short delay
        setTimeout(animateKPICards, 300);
        
        // Setup scroll animations
        animateChartsOnScroll();
        
        // Setup dataset selector
        handleDatasetSelection();
    }
    
    // Run initialization
    init();
    
    // Add subtle hover effects for interactive elements
    function addHoverEffects() {
        const interactiveElements = document.querySelectorAll('.kpi-card, .chart-card');
        
        interactiveElements.forEach(element => {
            element.addEventListener('mouseenter', function() {
                this.style.transition = 'all 0.2s ease';
            });
            
            element.addEventListener('mouseleave', function() {
                this.style.transition = 'all 0.2s ease';
            });
        });
    }
    
    addHoverEffects();
    
    console.log('Professional dashboard animations initialized');
});
