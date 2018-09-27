function processData(data) {
  return data.map(function (x) {
    return { y:x.value, x: new Date(x.time)};
  }).filter(function(x) {
    return x.y !== null;
  });
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

var datasets = [];

window.sensors.forEach(function (element) {
  var pointColor = element.name == "Light" ? window.chartColors.yellow : window.chartColors.blue;
  var avgColor = element.name == "Light" ? window.chartColors.orange : window.chartColors.purple;


  datasets.push({
    label: element.name,
    backgroundColor: pointColor,
    borderColor: pointColor,
    data: [],
    fill: false,
    showLine: false,
    id: element.id
  });
  datasets.push(
    {
      label: "Avg",
      backgroundColor: avgColor,
      borderColor: avgColor,
      data: [],
      fill: false,
      id: element.id + "-Avg"
    }
  );
});


var config = {
  type: 'line',
  data: { datasets: datasets },
  options: {
    responsive: true,
    title: {
      display: true,
      text: 'Sensors'
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

function addDataToChart(sensor_id, chart, data) {
  var processedData = processData(data)
  var averageData = chunk(processedData, 20).map(function (x) {
    var sumV = x.reduce(function(a,b) {return a + b.y }, 0)
    var sumT = x.reduce(function(a,b) {return a + b.x.getTime() }, 0)
    return {
      x: new Date(sumT / x.length),
      y: sumV / x.length
    }
  })

  var points = chart.data.datasets.find((x) => x.id == sensor_id)
  var averages = chart.data.datasets.find((x) => x.id == sensor_id + "-Avg")

  processedData.forEach((element) => points.data.push(element))
  averageData.forEach((element) => averages.data.push(element))
}


function loadData(sensor_id, page, chart, period) {
  var url = "/api/sensor/" + sensor_id + "?page=" + page + "&period=" + period
  return $.get(url)
}

function loadInParallel(sensor_id, i, period) {
  var before = new Date()
  $.when(
    loadData(sensor_id, i, chart, period),
    loadData(sensor_id, i + 1, chart, period)
  ).done(function (a1,a2) {
    // Benchmark:
    // console.log((new Date()).getTime() - before.getTime())

    if(a2[0].length > 0) {
      loadInParallel(sensor_id, i+2, period)
    }
    addDataToChart(sensor_id, chart, a1[0])
    chart.update()
    addDataToChart(sensor_id, chart, a2[0])
    chart.update()
  })
}

$(function () {
  var ctx = document.getElementById('canvas').getContext('2d');
  chart = new Chart(ctx, config);
  var period = location.hash.substr(1) || "historical"

  var loadAllData = function () {
    window.sensors.forEach(function (sensor) {
      loadInParallel(sensor.id, 0, period);
    })
  }

  $(".dropdown-item").click(function () {
    period = $(this).attr("href").substr(1)
    chart.data.datasets.forEach(function (dataset){
      dataset.data = [];
    });
    chart.update()
    loadAllData();
  })

  $("#irrigation-button").click(function () {
    var button = $(this);
    var oldHtml = button.html();
    button.html("Waiting...");
    var amount = $("#irrigation-amount").val();
    var url = "/gardener/irrigate/" + window.hose + "?amount=" + amount;
    $.post(url).done(function (response) {
      button.html(oldHtml);
    })
  })

  loadAllData();
})
