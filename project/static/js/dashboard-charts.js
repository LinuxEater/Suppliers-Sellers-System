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
                    backgroundColor: [
                        '#D4AF37', // Gold
                        '#2997ff', // Blue
                        '#34c38f', // Green
                        '#f46a6a', // Red
                        '#ffb629', // Orange
                    ],
                    borderColor: '#fff',
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

    // Line Chart: Sales over time
    const salesLineCtx = document.getElementById('salesLineChart');
    if (salesLineCtx && typeof salesChartData !== 'undefined') {
        new Chart(salesLineCtx, {
            type: 'line',
            data: {
                labels: salesChartData.labels,
                datasets: [{
                    label: 'Vendas (R$)',
                    data: salesChartData.data,
                    fill: true,
                    backgroundColor: 'rgba(41, 151, 255, 0.2)', // Light blue with transparency
                    borderColor: '#2997ff', // Blue
                    tension: 0.3,
                    pointBackgroundColor: '#2997ff',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#2997ff',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            color: '#212529' // Dark text for legend
                        }
                    },
                    title: {
                        display: false,
                        text: 'Vendas nos Últimos 30 Dias',
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

    // Bar Chart: Top 5 Vendors by Sales
    const vendorSalesBarCtx = document.getElementById('vendorSalesBarChart');
    if (vendorSalesBarCtx && typeof vendorSalesChartData !== 'undefined') {
        new Chart(vendorSalesBarCtx, {
            type: 'bar',
            data: {
                labels: vendorSalesChartData.labels,
                datasets: [{
                    label: 'Total de Vendas (R$)',
                    data: vendorSalesChartData.data,
                    backgroundColor: [
                        '#34c38f', // Green
                        '#f46a6a', // Red
                        '#ffb629', // Orange
                        '#6C757D', // Gray
                        '#D4AF37', // Gold
                    ],
                    borderColor: '#fff',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: false,
                        text: 'Top 5 Vendedores por Vendas',
                        color: '#212529'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: '#212529'
                        },
                        grid: {
                            color: '#DEE2E6'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#212529'
                        },
                        grid: {
                            color: '#DEE2E6'
                        }
                    }
                }
            }
        });
    }

    // Doughnut Chart: Top 5 Selling Products
    const topProductsDoughnutCtx = document.getElementById('topProductsDoughnutChart');
    if (topProductsDoughnutCtx && typeof topProductsChartData !== 'undefined') {
        new Chart(topProductsDoughnutCtx, {
            type: 'doughnut',
            data: {
                labels: topProductsChartData.labels,
                datasets: [{
                    data: topProductsChartData.data,
                    backgroundColor: [
                        '#D4AF37',
                        '#2997ff',
                        '#34c38f',
                        '#f46a6a',
                        '#ffb629',
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
                            color: '#212529'
                        }
                    },
                    title: {
                        display: false,
                        text: 'Top 5 Produtos Mais Vendidos',
                        color: '#212529'
                    }
                }
            }
        });
    }
});
