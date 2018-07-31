var data = window.sensor.data.map(function (x) {
  return { y:x.value, x: new Date(x.time * 1000) };
})

var config = {
  type: 'line',
  data: {
    // labels: labels,
    datasets: [{
      label: window.sensor.name,
      backgroundColor: window.chartColors.blue,
      borderColor: window.chartColors.blue,
      data: data,
      fill: false,
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
	  labelString: 'Month'
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
