//Set up SVG dimensions and properties
const margin = {top: 20, right: 10, bottom: 20, left: 20},
width = 350 - margin.left - margin.right,
height = 350 - margin.top - margin.bottom,
barPadding = 7,
graph_misc = {ylabel:4, xlabelH :4, title:12};


function updateBarChart(group, color, datasetBarChart){

    const currentBarChart = get_percentage(group, datasetBarChart);

    //Defining chart scale, same as the default bar chart
    const xScale = d3.scaleLinear()
        .domain([0, currentBarChart.length])
        .range([0, width]);

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(currentBarChart, function(d) { return d.value; })])
        .range([height,0]);

    const bar = d3.select('#barChart svg');  //Selecting the div containing bar chart ID and creating an SVG element

    // Add title to Barchart
    bar.selectAll("text.title")
        .attr("x", (width + margin.left + margin.right)/2)
        .attr('y', graph_misc.title+2)
        .attr("class","title")
        .attr("text-anchor", "middle")
        .text("details of negative reviews for "+group);

    const visualization = d3.select('barChartPlot')
        .datum(currentBarChart);    //binding data to multiple SVG elements

    visualization.selectAll('rect')
        .data(currentBarChart)
        .transition()
        .duration(750)
        .attr('x',  (width + margin.left + margin.right)/2)
        .attr('y', graph_misc.title+2)
        .attr('class', 'title')
        .attr('text-anchor', 'middle')
        .text('details of negative reviews for '+group);

    const plot = d3.select('#barChartPlot')
        .datum(currentBarChart);        //binding data to multiple SVG elements

    plot.selectAll('rect')
        .data(currentBarChart)
        .transition()       //Setting bar chart change transition
        .duration(800)
        .attr('x', function(d,i){
            return xScale(i);
        })
        .attr('width', width/currentBarChart.length - barPadding)
        .attr('y', function(d){
            return yScale(d.value)
        })
        .attr("height", function(d) {
            return height-yScale(d.value);
        })
        .attr("fill", color);

    plot.selectAll("text.yAxis")
        .data(currentBarChart)
        .transition()
        .duration(750)
        .attr("text-anchor", "middle")
        .attr("x", function(d, i) {
            return (i * (width / currentBarChart.length)) + ((width / currentBarChart.length - barPadding) / 2);})
        .attr("y", function(d) {
            return yScale(d.value) - graph_misc.ylabel;})
        .text(function(d) {
        return d.value+'%';})
        .attr("class", "yAxis");
};