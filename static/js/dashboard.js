// Dataset selection handler
function changeDataset() {
    const select = document.getElementById('dataset-select');
    const selectedDataset = select.value;
    
    // Reload page with new dataset parameter
    window.location.href = `/dashboard?dataset=${selectedDataset}`;
}

// Add smooth scroll behavior
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for any internal links
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
    
    // Add animation to cards on load
    const cards = document.querySelectorAll('.card, .insight-card, .explanation-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 50);
    });
});
