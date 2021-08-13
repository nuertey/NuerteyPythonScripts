function tracciaGrafico() {
    data = [];
    trace = [];
    indexTrace = 0;

    // Cleanup only if not first start (else it is already clean, and this would raise an error):
    if (FirstStart) {
        FirstStart = false;
    } else { // Clear chart before plotting if it has already peing plotted.
        Plotly.deleteTraces('myDiv', clearData);
        clearData = [];
    }


    Squadre.forEach(function(squadra) {
        trace[indexTrace] = puntiSquadraCumulativi[squadra]; // Copy trace data from my source array
        data.push(
            {
                x: xArray, 
                y: puntiSquadraCumulativi[squadra], 
                type: "scatter", 
                name: squadra, // from "forEach"
                line: {width: 5}
            }
        ); // Add trace to data array
        clearData.push(indexTrace); // Add trace index to array I will use to clean the old chart
        indexTrace++;
    });
    Plotly.newPlot('myDiv', data); // Plot data
}

# While building the chart I build an array (clearData) which then I can use to clear the chart: it just containing all the indexes of all the traces, and it is the argument of Plotly.deleteTraces('myDiv', clearData);
# 
# But maybe you actually don't want to delete traces but just update them:

https://plot.ly/javascript/plotlyjs-function-reference/#plotlyupdate

https://stackoverflow.com/questions/32116368/plotly-update-data

https://stackoverflow.com/questions/35946484/high-performance-way-to-update-graph-with-new-data-in-plotly
