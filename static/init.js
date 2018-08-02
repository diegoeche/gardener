function processData(data) {
  return data.map(function (x) {
    return { y:x.value, x: new Date(x.time * 1000)};
  })
}

function chunk(array, size) {
  var current = array.slice();
  var resultArray = [];
  var chunkSize = current.length/size;
  for(i=0; i < chunkSize; i++) {
    resultArray.push(current.splice(0, size));
  }
  return resultArray;
}

var config = {
  type: 'line',
  data: {
    datasets: [{
      label: window.sensor.name,
      backgroundColor: window.chartColors.blue,
      borderColor: window.chartColors.blue,
      data: [],
      fill: false,
      showLine: false
    },
    {
      label: "Average",
      backgroundColor: window.chartColors.red,
      borderColor: window.chartColors.red,
      data: [],
      fill: false
    }]
  },
  options: {
    responsive: true,
    title: {
      display: true,
      text: 'Humidity'
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true
    },
    scales: {
      xAxes: [{
	type: "time",
	display: true,
	scaleLabel: {
	  display: true,
	  labelString: 'Time'
	}
      }],
      yAxes: [{
	display: true,
	scaleLabel: {
	  display: true,
	  labelString: 'Value'
	}
      }]
    }
  }
};

var chart;

function addDataToChart(chart, data) {
  var processedData = processData(data)
  var averageData = chunk(processedData, 20).map(function (x) {
    var sumV = x.reduce(function(a,b) {return a + b.y }, 0)
    var sumT = x.reduce(function(a,b) {return a + b.x.getTime() }, 0)
    return {
      x: new Date(sumT / x.length),
      y: sumV / x.length
    }
  })

  var points = chart.data.datasets[0]
  var averages = chart.data.datasets[1]

  processedData.forEach((element) => points.data.push(element))
  averageData.forEach((element) => averages.data.push(element))
}


function loadData(page, chart) {
  return $.get("/api?page=" + page)
}

var allDataLoaded = false;

function loadInParallel(i) {
  $.when(
    loadData(i, chart),
    loadData(i + 1, chart),
    loadData(i + 2, chart),
    loadData(i + 3, chart)
  ).done(function (a1,a2,a3,a4) {
    if(a3[0].length > 0) {
      console.log(i)
      loadInParallel(i+4)
    }
    addDataToChart(chart, a1[0])
    chart.update()
    addDataToChart(chart, a2[0])
    chart.update()
    addDataToChart(chart, a3[0])
    chart.update()
    addDataToChart(chart, a4[0])
    chart.update()
  })
}

$(function () {
  var ctx = document.getElementById('canvas').getContext('2d');
  chart = new Chart(ctx, config);

  var i = 0;
  loadInParallel(0);

  console.log("here?")
})
