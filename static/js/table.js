d3.csv("static/data/Kaggle_TwitterUSAirlineSentiment.csv", function(error, data) {
    if (error) throw error;
    let sortAscending = true;
    let table = d3.select('#page-wrap').append('table');
    let titles = d3.keys(data[0]);
    let headers = table.append('thead').append('tr').selectAll('th').data(titles)
                .enter().append('th')
                .text(function (d) {
                    return d;
                }).on('click', function (d) {
                    headers.attr('class', 'header');

                    if (sortAscending) {
                        rows.sort(function(a, b) {return d3.ascending(b[d], a[d]);  });
                        sortAscending = false;
                        this.className = 'aes';
                        }
                    else {
                        rows.sort(function(a, b) { return d3.descending(b[d], a[d]); });
                        sortAscending = true;
                        this.className = 'des';
                        }
                });
    let rows = table.append('tbody').selectAll('tr').data(data).enter().append('tr');
    rows.selectAll('td').data(function (d) {
        return titles.map(function (k) {
            return { 'value': d[k], 'name': k};
        });
    }).enter().append('td').attr('data-th', function (d) {
        return d.name;
    }).text(function (d) {
        return d.value;
    });
});