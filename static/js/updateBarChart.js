function updateBarChart(group = "All", color ="#757077", datasetBarChart){
    d3.select('#barChart svg').remove();
    defaultBarChart = get_percentage(group, datasetBarChart);

    const xScale = d3.scaleLinear()     // Barchart X axis scale
        .domain([0, defaultBarChart.length]) // Scale range from 0 to the length of data object
        .range([0, width]);

    const yScale = d3.scaleLinear() // Barchart y axis scale
        .domain([0, d3.max(defaultBarChart, function(d) { return d.value; })])    //Scale range from 0 to the maximum value of the default bar chart data
        .range([height, 0]);

    // // Selecting the div with id barChart on the index.html template file
    const bar = d3.select('#barChart')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .attr('id', 'barChartPlot');

    //Adding barchart title
    bar.append('text')
        .attr('x', (width + margin.left + margin.right)/2)
        .attr('y', graph_misc.title)
        .attr('class','title')
        .attr('text-anchor', 'middle')
        .text('Details of '+ group + ' negative reviews');

    const visualization = bar.append('g')
        .attr("transform", "translate(" + margin.left + "," + (margin.top + graph_misc.ylabel) + ")");

    //Selecting all the bar serving as bins of data
    visualization.selectAll("rect")
        .data(defaultBarChart)
        .enter()
        .append("rect")
        .attr("x", function(d, i) {
            return xScale(i);
        })
        .attr("width", width / defaultBarChart.length - barPadding)
        .attr("y", function(d) {
            return yScale(d.value);
        })
        .attr("height", function(d) {
            return height-yScale(d.value);
        })
        .attr("fill", color);

    //Adding  barchart labels
    visualization.selectAll('text')
        .data(defaultBarChart)
        .enter()
        .append("text")
        .text(function(d) {
                return d.value+"%";
        })
        .attr("text-anchor", "middle")

        .attr("x", function(d, i) {
                return (i * (width / defaultBarChart.length)) + ((width / defaultBarChart.length - barPadding) / 2);
        })
        .attr("y", function(d) {
                return (yScale(d.value) - graph_misc.ylabel); //Setting the Y axis to represent the value in the served JSON data
        })
        .attr("class", "yAxis");


    const xLabels = bar
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + (margin.top + height + graph_misc.xlabelH)  + ")");

    xLabels.selectAll("text.xAxis")
        .data(defaultBarChart)
        .enter()
        .append("text")
        .text(function(d) { return d.category;})
        .attr("text-anchor", "middle")
        .attr("x", function(d, i) {
            return (i * (width / defaultBarChart.length)) + ((width / defaultBarChart.length - barPadding) / 2);
        })
        .attr("y", 15)
        .attr("class", "xAxis");
}