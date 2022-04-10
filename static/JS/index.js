function draw(){
    $.post("https://capstone-smart-meter.herokuapp.com/vars", {}, (d, s)=>{
        var trace1 = {
            y: d["voltage"],
            type: 'scatter'
        };
    
        var trace2 = {
            y: d["current"],
            type: 'scatter'
        };
    
        Plotly.newPlot('voltage', [trace1], {title:"Voltage"}, {responsive: true});
        Plotly.newPlot('current', [trace2], {title:"Current"}, {responsive: true});
        document.getElementById("hz").innerHTML = d["Frequency"];
        document.getElementById("pf").innerHTML = d["Power Factor"];
    })
};
