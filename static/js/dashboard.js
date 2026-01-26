// Load and render charts
async function loadCharts(dataset = "stock_1.csv") {
    try {
        const res = await fetch(`/api/chart-data?dataset=${dataset}`);
        const d = await res.json();
        
        // PRICE + MAs
        Plotly.newPlot("priceChart", [
            { 
                x: d.dates, 
                y: d.close, 
                name: "Close Price", 
                mode: "lines",
                line: { color: "#667eea", width: 2 }
            },
            { 
                x: d.dates, 
                y: d.ma_short, 
                name: "MA(3)", 
                mode: "lines",
                line: { color: "#4caf50", width: 2, dash: "dash" }
            },
            { 
                x: d.dates, 
                y: d.ma_long, 
                name: "MA(5)", 
                mode: "lines",
                line: { color: "#f44336", width: 2, dash: "dot" }
            },
        ], { 
            title: "Price with Moving Averages",
            xaxis: { title: "Date" },
            yaxis: { title: "Price ($)" },
            hovermode: "x unified",
            plot_bgcolor: "#f8f9fa",
            paper_bgcolor: "white"
        });
        
        // RETURNS
        const returnColors = d.returns.map(r => r >= 0 ? "#4caf50" : "#f44336");
        Plotly.newPlot("returnsChart", [
            { 
                x: d.dates, 
                y: d.returns, 
                name: "Daily Return (%)", 
                type: "bar",
                marker: { color: returnColors }
            }
        ], { 
            title: "Daily Returns (%)",
            xaxis: { title: "Date" },
            yaxis: { title: "Return (%)" },
            plot_bgcolor: "#f8f9fa",
            paper_bgcolor: "white"
        });
        
        // VOLATILITY
        Plotly.newPlot("volChart", [
            { 
                x: d.dates, 
                y: d.volatility, 
                name: "Rolling Volatility (%)", 
                mode: "lines",
                fill: "tozeroy",
                line: { color: "#ff9800", width: 2 }
            }
        ], { 
            title: "Rolling Volatility (%)",
            xaxis: { title: "Date" },
            yaxis: { title: "Volatility (%)" },
            plot_bgcolor: "#f8f9fa",
            paper_bgcolor: "white"
        });
    } catch (error) {
        console.error("Error loading charts:", error);
    }
}

// Dataset selection handler
function changeDataset() {
    const select = document.getElementById('dataset-select');
    const selectedDataset = select.value;
    
    // Reload page with new dataset parameter
    window.location.href = `/dashboard?dataset=${selectedDataset}`;
}

// Add smooth scroll behavior
document.addEventListener('DOMContentLoaded', function() {
    // Load charts on page load
    const urlParams = new URLSearchParams(window.location.search);
    const currentDataset = urlParams.get('dataset') || 'stock_1.csv';
    loadCharts(currentDataset);
    
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
