document.addEventListener('DOMContentLoaded', function() {
    // Chart.js global settings for light theme
    Chart.defaults.color = '#212529'; // Dark text for light background
    Chart.defaults.borderColor = '#DEE2E6'; // Light border for light background

    // Pie Chart: Products by Supplier
    const supplierPieCtx = document.getElementById('supplierPieChart');
    if (supplierPieCtx && typeof pieChartData !== 'undefined') {
        new Chart(supplierPieCtx, {
            type: 'pie',
            data: {
                labels: pieChartData.labels,
                datasets: [{
                    data: pieChartData.data,
                    backgroundColor: [
                        '#D4AF37', // Gold
                        '#2997ff', // Blue
                        '#34c38f', // Green
                        '#f46a6a', // Red
                        '#ffb629', // Orange
                        '#6C757D', // Gray
                    ],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#212529' // Dark text for legend
                        }
                    },
                    title: {
                        display: false,
                        text: 'Produtos por Fornecedor',
                        color: '#212529' // Dark text for title
                    }
                }
            }
        });
    }

    // Bar Chart: Top 5 Products by Stock
    const stockBarCtx = document.getElementById('stockBarChart');
    if (stockBarCtx && typeof barChartData !== 'undefined') {
        new Chart(stockBarCtx, {
            type: 'bar',
            data: {
                labels: barChartData.labels,
                datasets: [{
                    label: 'Estoque',
                    data: barChartData.data,
                    backgroundColor: '#D4AF37', // Gold
                    borderColor: '#D4AF37',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false,
                        labels: {
                            color: '#212529' // Dark text for legend
                        }
                    },
                    title: {
                        display: false,
                        text: 'Top 5 Produtos em Estoque',
                        color: '#212529' // Dark text for title
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: '#212529' // Dark text for ticks
                        },
                        grid: {
                            color: '#DEE2E6' // Light grid lines
                        }
                    },
                    x: {
                        ticks: {
                            color: '#212529' // Dark text for ticks
                        },
                        grid: {
                            color: '#DEE2E6' // Light grid lines
                        }
                    }
                }
            }
        });
    }
});
