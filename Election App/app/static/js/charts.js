/* global Chart */

const wrapper = document.querySelector('.charts-div');
const barChartCanvas = wrapper.querySelector('.bar-chart');
const doughnutChartCanvas = wrapper.querySelector('.doughnut-chart');

export function initCharts() {
    createEmptyBarChart();
    createEmptyDoughnutChart();
}

export function setChartData(data) {
    let chartLabels = [];
    let chartData = [];
    let chartColors = [];

    data.forEach(item => {
        chartLabels.push(item.shortname);
        chartData.push(item.num_of_votes);
        chartColors.push(item.color);
    });

    let barChart = Chart.getChart(barChartCanvas);
    let doughnutChart = Chart.getChart(doughnutChartCanvas);

    //Set labels
    barChart.data.labels = chartLabels;
    doughnutChart.data.labels = chartLabels;
    
    //Set data
    barChart.data.datasets[0].data = chartData;
    doughnutChart.data.datasets[0].data = chartData;

    //Update bar chart Y axis range
    let minDataVal =  Math.min(...data);
    let maxDataVal =  Math.max(...data);
    barChart.options.scales.y.min = Math.floor(minDataVal / 10) * 10;
    barChart.options.scales.y.max = Math.ceil(maxDataVal / 10) * 10;

    //Set data colors
    barChart.data.datasets[0].backgroundColor = chartColors;
    doughnutChart.data.datasets[0].backgroundColor = chartColors;

    //Enable tooltips for doughnut chart
    doughnutChart.options.plugins.tooltip.enabled = true;

    barChart.update();
    doughnutChart.update();
}

function createEmptyBarChart() {
    const ctx = barChartCanvas.getContext('2d');

    const config = {
        type: 'bar',

        data: {
            labels: [],
            datasets: [{
                data: [],
            }]
        },

        options: {
            maintainAspectRatio: false,
            scales: {
                y: {
                    min: 0,
                    max: 100
                }
            },
            plugins: {
                fullsize: true,
                legend: {
                    display: false
                }
            }
        }
    }

    new Chart(ctx, config);
}

function createEmptyDoughnutChart() {
    const ctx = doughnutChartCanvas.getContext('2d');

    const config = {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [1]
            }]
        },
        
        options: {
            plugins: {
                fullsize: true,
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    };

    new Chart(ctx, config);
}

/*
    ogolnie w po updacie danych rozmiar canvasow sie nie zmniejsza (300x300 zostaje)
    ale zaczyna includowac w tym legende/opisy osi wiec defacto rozmiar wykresow
    sie zmniejsza.
*/