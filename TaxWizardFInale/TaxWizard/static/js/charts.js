document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts if elements exist
    if (document.getElementById('taxDistributionChart')) {
        renderTaxDistributionChart();
    }
    
    if (document.getElementById('deductionsChart')) {
        renderDeductionsChart();
    }
    
    if (document.getElementById('savingsComparisonChart')) {
        renderSavingsComparisonChart();
    }
});

function renderTaxDistributionChart() {
    const ctx = document.getElementById('taxDistributionChart').getContext('2d');
    
    // Get data from the chart element's data attributes
    const chartElement = document.getElementById('taxDistributionChart');
    const income = parseFloat(chartElement.dataset.income || 0);
    const taxLiability = parseFloat(chartElement.dataset.taxLiability || 0);
    const remaining = income - taxLiability;
    
    const taxDistributionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Tax Liability', 'Remaining Income'],
            datasets: [{
                data: [taxLiability, remaining],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(75, 192, 192, 0.6)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ₹${value.toLocaleString()} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function renderDeductionsChart() {
    const ctx = document.getElementById('deductionsChart').getContext('2d');
    
    // Get data from the chart element's data attributes
    const chartElement = document.getElementById('deductionsChart');
    const mortgageInterest = parseFloat(chartElement.dataset.mortgageInterest || 0);
    const propertyTax = parseFloat(chartElement.dataset.propertyTax || 0);
    const charitableContributions = parseFloat(chartElement.dataset.charitableContributions || 0);
    const medicalExpenses = parseFloat(chartElement.dataset.medicalExpenses || 0);
    const otherDeductions = parseFloat(chartElement.dataset.otherDeductions || 0);
    
    const deductionsChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Mortgage Interest', 'Property Tax', 'Charitable Contributions', 'Medical Expenses', 'Other Deductions'],
            datasets: [{
                data: [mortgageInterest, propertyTax, charitableContributions, medicalExpenses, otherDeductions],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            return `${label}: ₹${value.toLocaleString()}`;
                        }
                    }
                }
            }
        }
    });
}

function renderSavingsComparisonChart() {
    const ctx = document.getElementById('savingsComparisonChart').getContext('2d');
    
    // Get data from the chart element's data attributes
    const chartElement = document.getElementById('savingsComparisonChart');
    const currentTax = parseFloat(chartElement.dataset.currentTax || 0);
    const optimizedTax = parseFloat(chartElement.dataset.optimizedTax || 0);
    const savings = currentTax - optimizedTax;
    
    const labels = ['Current Tax', 'Optimized Tax', 'Potential Savings'];
    const data = [currentTax, optimizedTax, savings];
    const backgroundColors = [
        'rgba(255, 99, 132, 0.6)',
        'rgba(75, 192, 192, 0.6)',
        'rgba(255, 206, 86, 0.6)'
    ];
    const borderColors = [
        'rgba(255, 99, 132, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(255, 206, 86, 1)'
    ];
    
    const savingsComparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Amount (₹)',
                data: data,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
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
                            return '₹' + value.toLocaleString();
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return '₹' + context.raw.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}
