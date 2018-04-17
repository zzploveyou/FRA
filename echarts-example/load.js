//初始化加载

var node_num;
var edge_num;
$(function () {
    first_init();

});

function first_init() {
    var html = "";
    for (var i = 2018; i >= 1995; i--) {
        if (i == 2017) {
            html += "<option value='data_" + i + "' name='data' selected='selected'>" + i + "</option>";
        } else {
            html += "<option value='data_" + i + "' name='data'>" + i + "</option>";
        }
    }
    $("#datas").html(html);
    var html = "<option value='true' name='label'>true</option>";
    html += "<option value='false' selected='selected' name='label'>false</option>";
    $("#labels").html(html);
    init();
}

function init() {
    var networkData;
    var select_data = $("#datas").val();
    switch (select_data) {
        case 'data_2018':
            networkData = data_2018;
            break;
        case 'data_2017':
            networkData = data_2017;
            break;
        case 'data_2016':
            networkData = data_2016;
            break;
        case 'data_2015':
            networkData = data_2015;
            break;
        case 'data_2014':
            networkData = data_2014;
            break;
        case 'data_2013':
            networkData = data_2013;
            break;
        case 'data_2012':
            networkData = data_2012;
            break;
        case 'data_2011':
            networkData = data_2011;
            break;
        case 'data_2010':
            networkData = data_2010;
            break;
        case 'data_2009':
            networkData = data_2009;
            break;
        case 'data_2008':
            networkData = data_2008;
            break;
        case 'data_2007':
            networkData = data_2007;
            break;
        case 'data_2006':
            networkData = data_2006;
            break;
        case 'data_2005':
            networkData = data_2005;
            break;
        case 'data_2004':
            networkData = data_2004;
            break;
        case 'data_2003':
            networkData = data_2003;
            break;
        case 'data_2002':
            networkData = data_2002;
            break;
        case 'data_2001':
            networkData = data_2001;
            break;
        case 'data_2000':
            networkData = data_2000;
            break;
        case 'data_1999':
            networkData = data_1999;
            break;
        case 'data_1998':
            networkData = data_1998;
            break;
        case 'data_1997':
            networkData = data_1997;
            break;
        case 'data_1996':
            networkData = data_1996;
            break;
        case 'data_1995':
            networkData = data_1995;
            break;
    }

    // node limit number
    var node_limit = $("#node_limit").val();
    if (node_limit == "" || node_limit == null) {
        node_num = 10000;
    } else {
        node_num = node_limit * 1;
    }
    // edge limit number
    var edge_limit = $("#edge_limit").val();
    if (edge_limit == "" || edge_limit == null) {
        edge_num = 10000;
    } else {
        edge_num = edge_limit * 1;
    }
    // show node label
    var show_tabel = false;
    if($("#labels").val() == 'true'){
        show_tabel = true;
    }

    var myChart = echarts.init(document.getElementById('network'));

    var option = {
        legend: {
            data: networkData.legend
        },
        series: [{
            type: 'graph',
            roam: true,
            draggable: false,
            focusNodeAdjacency: true,
            nodeScaleRatio: 0,
            layout: 'force',
            force: {
                initLayout: 'force',
                layoutAnimation: false,
                repulsion: 50,
                edgeLength: 5,
                gravity: 0.5
            },
            label: {
                normal: {
                    show: show_tabel,
                    position: 'bottom',
                    formatter: '{b}'
                }
            },
            data: networkData.nodes.slice(0, node_num).map(function (node, idx) {
                node.id = idx;
                return node;
            }),
            edges: networkData.links.slice(0, edge_num),
            categories: networkData.categories,

        }]
    };
    // console.log(networkData.links.slice(0, edge_num));
    myChart.setOption(option);
}
