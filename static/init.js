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
      backgroundColor: window.chartColors.purple,
      borderColor: window.chartColors.purple,
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
	  labelString: ''
	},
	time: {
	  displayFormats: {
            hour: 'MMM D - hA'
          }
	}
      }],
      yAxes: [{
	display: true,
	scaleLabel: {
	  display: true,
	  labelString: ''
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


function loadData(page, chart, period) {
  var url = "/api?page=" + page + "&period=" + period
  console.log(url)
  return $.get(url)
}

function loadInParallel(i, period) {
  var before = new Date()
  $.when(
    loadData(i,     chart, period),
    loadData(i + 1, chart, period),
    loadData(i + 2, chart, period),
    loadData(i + 3, chart, period)
  ).done(function (a1,a2,a3,a4) {
    console.log((new Date()).getTime() - before.getTime())

    if(a3[0].length > 0) {
      loadInParallel(i+4, period)
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
  var period = location.hash.substr(1) || "historical"

  $(".dropdown-item").click(function () {
    period = $(this).attr("href").substr(1)
    chart.data.datasets[0].data = [];
    chart.data.datasets[1].data = [];
    chart.update()
    loadInParallel(0, period);
  })

  $("#irrigation-button").click(function () {
    $.post("/gardener/irrigate").done(function (response) {
      console.log(response);
    })
  })

  loadInParallel(0, period);
})
