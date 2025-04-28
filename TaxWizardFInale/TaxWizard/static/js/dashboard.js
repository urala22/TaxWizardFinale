document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Tax data visualization
    if (document.getElementById('taxDataChart')) {
        renderTaxDataChart();
    }

    // Tax optimization chart
    if (document.getElementById('optimizationChart')) {
        renderOptimizationChart();
    }
});

function renderTaxDataChart() {
    const ctx = document.getElementById('taxDataChart').getContext('2d');
    
    // Get data from data attributes
    const chartElement = document.getElementById('taxDataChart');
    const income = parseFloat(chartElement.dataset.income || 0);
    const deductions = parseFloat(chartElement.dataset.deductions || 0);
    const taxableIncome = parseFloat(chartElement.dataset.taxableIncome || 0);
    const taxLiability = parseFloat(chartElement.dataset.taxLiability || 0);
    
    const taxDataChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Income', 'Deductions', 'Taxable Income', 'Tax Liability'],
            datasets: [{
                label: 'Amount ($)',
                data: [income, deductions, taxableIncome, taxLiability],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 99, 132, 0.6)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function renderOptimizationChart() {
    const ctx = document.getElementById('optimizationChart').getContext('2d');
    
    // Get data from data attributes
    const chartElement = document.getElementById('optimizationChart');
    const currentTax = parseFloat(chartElement.dataset.currentTax || 0);
    const optimizedTax = parseFloat(chartElement.dataset.optimizedTax || 0);
    const potentialSavings = currentTax - optimizedTax;
    
    const optimizationChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Current Tax', 'Optimized Tax', 'Potential Savings'],
            datasets: [{
                label: 'Amount ($)',
                data: [currentTax, optimizedTax, potentialSavings],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(255, 206, 86, 0.6)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}