var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
var config = {
  type: 'line',
  data: {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [{
      label: 'Humidity',
      backgroundColor: window.chartColors.blue,
      borderColor: window.chartColors.blue,
      data: [
	randomScalingFactor(),
	randomScalingFactor(),
	randomScalingFactor(),
	randomScalingFactor(),
	randomScalingFactor(),
	randomScalingFactor(),
	randomScalingFactor()
      ],
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
