let feedbackRatingChart;
let feedbackDistributionChart;
let feedbackTrendChart;


function initCharts(data) {
    if (!data) return;

    renderRatingChart(data.ratings);
    renderDistributionChart(data.distribution);
    renderTrendChart(data.trend);
}

function renderRatingChart(ratings) {
    const ctx = document.getElementById("ratingChart");
    if (!ctx) return;

    if (feedbackRatingChart) feedbackRatingChart.destroy();

    feedbackRatingChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ratings.labels, // e.g. ["Teacher A", "Teacher B"]
            datasets: [{
                label: "Average Rating",
                data: ratings.values, // e.g. [4.2, 3.8]
                backgroundColor: "rgba(54, 162, 235, 0.6)",
                borderColor: "rgba(54, 162, 235, 1)",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true },
                title: {
                    display: true,
                    text: "Faculty Average Ratings"
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 5
                }
            }
        }
    });
}

function renderDistributionChart(distribution) {
    const ctx = document.getElementById("distributionChart");
    if (!ctx) return;

    if (feedbackDistributionChart) feedbackDistributionChart.destroy();

    feedbackDistributionChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: distribution.labels, // ["Positive", "Neutral", "Negative"]
            datasets: [{
                data: distribution.values, // [60, 25, 15]
                backgroundColor: [
                    "#28a745",
                    "#ffc107",
                    "#dc3545"
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: "Feedback Distribution"
                }
            }
        }
    });
}

function renderTrendChart(trend) {
    const ctx = document.getElementById("trendChart");
    if (!ctx) return;

    if (feedbackTrendChart) feedbackTrendChart.destroy();

    feedbackTrendChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: trend.labels, // ["Jan", "Feb", "Mar"]
            datasets: [{
                label: "Feedback Count",
                data: trend.values, // [20, 35, 50]
                fill: true,
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                borderColor: "rgba(75, 192, 192, 1)",
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: "Feedback Trend Over Time"
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function loadSampleChartData() {
    const sampleData = {
        ratings: {
            labels: ["Prof. Sharma", "Prof. Khan", "Prof. Rai", "Prof. Joshi"],
            values: [4.5, 3.8, 4.2, 4.0]
        },
        distribution: {
            labels: ["Positive", "Neutral", "Negative"],
            values: [70, 20, 10]
        },
        trend: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            values: [30, 45, 50, 60, 75, 90]
        }
    };

    initCharts(sampleData);
}


document.addEventListener("DOMContentLoaded", function () {
    
});