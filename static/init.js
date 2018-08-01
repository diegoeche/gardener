var data = window.sensor.data.map(function (x) {
  return { y:x.value, x: new Date(x.time * 1000)};
})

function chunk(array, size) {
  var current = array.slice();
  var resultArray = [];
  var chunkSize = current.length/size;
  for(i=0; i < chunkSize; i++) {
    resultArray.push(current.splice(0, size));
  }
  return resultArray;
}

var averageData = chunk(data, 20).map(function (x) {
  var sumV = x.reduce(function(a,b) {return a + b.y }, 0)
  var sumT = x.reduce(function(a,b) {return a + b.x.getTime() }, 0)

  return {
    x: new Date(sumT / x.length),
    y: sumV / x.length
  }
})

console.log(data.length)
var config = {
  type: 'line',
  data: {
    datasets: [{
      label: window.sensor.name,
      backgroundColor: window.chartColors.blue,
      borderColor: window.chartColors.blue,
      data: data,
      fill: false,
      showLine: false
    },
    {
      label: "Average",
      backgroundColor: window.chartColors.red,
      borderColor: window.chartColors.red,
      data: averageData,
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


window.onload = function() {
  var ctx = document.getElementById('canvas').getContext('2d');
  window.myLine = new Chart(ctx, config);
};
