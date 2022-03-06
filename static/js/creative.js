const url = [pieChartDataUrl, barChartDataUrl];

Promise.all(url.map(url => d3.json(url))).then(run);

function run(dataset) {
    d3PieChart(dataset[0], dataset[1]);
    d3BarChart(dataset[1]);
};

// Please note this is just a handler to get the data as a promise, the code for the creative view is actually
// in pieChart.js