function main(){
    var dcs_from_data = document.getElementById('dcs-from-data')
    var attribute = document.getElementById('attribute')
    if(attribute)
        attribute = JSON.parse(attribute.textContent)

    if(dcs_from_data){
        var dcs = JSON.parse(dcs_from_data.textContent);
        if(!dcs.isComplex)
            dependency_graph(dcs, attribute)
    }

    var dcs_to_data = document.getElementById('dcs-to-data')
    if(dcs_to_data){
        var dcs = JSON.parse(dcs_to_data.textContent);
        if(!dcs.isComplex)
            dependent_graph(dcs, attribute)
    }

    if(document.getElementById('stats_pie_chart'))
        pie();

    var dependencyGraphLoaders = document.getElementsByClassName("dependency-graph-loader")
    for(var i=0; i<dependencyGraphLoaders.length; i++){
        dependencyGraphLoaders[i].addEventListener("click", function(){
            console.log("ajax1")
            $.ajax({
                url: 'http://localhost:8000/modules/attribute/' + attribute.id + '/dependency_ajax',
                method: 'GET',
                success: function(dcs){
                    document.getElementById('loader1').style.display = "block";
                    dependency_graph(dcs.dcs_from, dcs.attribute)
                },
                error: function(error){
                    console.log(error)
                }
            })
        })
    }

    var dependentGraphLoaders = document.getElementsByClassName("dependent-graph-loader")
    for(var i=0; i<dependentGraphLoaders.length; i++){
        dependentGraphLoaders[i].addEventListener("click", function(){
            console.log("ajax2")
            $.ajax({
                url: 'http://localhost:8000/modules/attribute/' + attribute.id + '/dependent_ajax',
                method: 'GET',
                success: function(dcs){
                    document.getElementById('loader2').style.display = "block";
                    dependent_graph(dcs.dcs_to, dcs.attribute)
                },
                error: function(error){
                    console.log(error)
                }
            })
        })
    }
}

function dependency_graph(dcs, attribute){
    node_list = []
    root_node = {id: attribute.name, label: attribute.name, color: "#f3af42"}
    node_list.push(root_node)
    for(var i=0; i<dcs.unique.length; i++){
        node = {id: dcs.unique[i], label: dcs.unique[i]}
        node_list.push(node)
    }
    var nodes = new vis.DataSet(node_list)

    edge_list = []
    for(var i=0; i<dcs.path.length; i++){
        path = dcs.path[i].reverse()
        for(var j=0; j<path.length-1; j++){
            edge = {from: path[j], to: path[j+1]}
            edge_list.push(edge)
        }
        root_edge = {from: path[path.length-1], to: root_node.id}
        edge_list.push(root_edge)
    }
    var edges = new vis.DataSet(edge_list)

    var container = document.getElementById('dependency-graph');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
        edges: {
            arrows: 'to'
        }
    };

    var network = new vis.Network(container, data, options);
    network.once("afterDrawing", function(){
        document.getElementById('loader1').style.display = "none";
    })
}

function dependent_graph(dcs, attribute){
    node_list = []
    console.log(attribute)
    root_node = {id: attribute.name, label: attribute.name, color: "#f3af42"}
    node_list.push(root_node)
    for(var i=0; i<dcs.unique.length; i++){
        node = {id: dcs.unique[i], label: dcs.unique[i]}
        node_list.push(node)
    }
    var nodes = new vis.DataSet(node_list)

    edge_list = []
    for(var i=0; i<dcs.path.length; i++){
        path = dcs.path[i].reverse()
        root_edge = {from: root_node.id, to: path[0]}
        edge_list.push(root_edge)
        for(var j=0; j<path.length-1; j++){
            edge = {from: path[j], to: path[j+1]}
            edge_list.push(edge)
        }
    }
    var edges = new vis.DataSet(edge_list)

    var container = document.getElementById('dependent-graph');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
        edges: {
            arrows: 'to'
        }
    };
    var network = new vis.Network(container, data, options);
    network.once("afterDrawing", function(){
        document.getElementById('loader2').style.display = "none";
    })
}

function pie(){
    var stats = JSON.parse(document.getElementById('pie-chart-data').textContent);
    values = []
    labels = []
    for(var key in stats){
        labels.push(key)
        values.push(stats[key])
    }
    var data = {
            datasets: [{
                data: values,
                backgroundColor: ['#cdc7ff', '#b5ce92', '#6faa6a', '#7ad5c3', '#ffb35c', '#eb91b4']
            }],
            labels: labels
    };

    var options = {
       tooltips: {
         enabled: true,
       },
       plugins: {
         datalabels: {
           formatter: (value, ctx) => {
             let datasets = ctx.chart.data.datasets;
             if (datasets.indexOf(ctx.dataset) === datasets.length - 1) {
               let sum = datasets[0].data.reduce((a, b) => a + b, 0);
               let percentage = Math.round((value / sum) * 100) + '%';
               return percentage;
             } else {
               return percentage;
             }
           },
           color: 'black',
         }
       },
    };

    var ctx = document.getElementById('stats_pie_chart').getContext('2d');
    var stats_pie_chart = new Chart(ctx, {
        type: 'pie',
        data: data,
        options: options
    })

}
window.onload = main;