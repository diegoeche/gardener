function loadData() {
  var url = "/api/sensors";
  return $.get(url)
}

$(function () {
  var ctx = document.getElementById('canvas').getContext('2d');
  var config = {
    type: 'bar',
    data: {
      labels: [],
      datasets: [{
	label: "Humidity",
	data: [],
	backgroundColor: [
	  'rgba(255, 99, 132, 0.2)',
	  'rgba(54, 162, 235, 0.2)',
	  'rgba(255, 206, 86, 0.2)',
	  'rgba(75, 192, 192, 0.2)',
	  'rgba(153, 102, 255, 0.2)',
	  'rgba(255, 159, 64, 0.2)'
	],
	borderColor: [
	  'rgba(255,99,132,1)',
	  'rgba(54, 162, 235, 1)',
	  'rgba(255, 206, 86, 1)',
	  'rgba(75, 192, 192, 1)',
	  'rgba(153, 102, 255, 1)',
	  'rgba(255, 159, 64, 1)'
	],
	borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: {
	yAxes: [{
          ticks: {
            min: 0.0,
            max: 1.0
          }
	}]
      }
    }
  };
  window.chart = new Chart(ctx, config);

  var loadAndSetData = function () {
    $.when(
      loadData(),
    ).done(function (data) {
      console.log(data)

      data = data.map(function (elem) {
        return {
	  "x": elem.name,
	  "y": elem.value
        };
      });

      var dataset = chart.data.datasets[0];
      dataset.data = [];
      chart.data.labels = data.map((x) => x.x)
      data.forEach((element) => dataset.data.push(element))
      chart.update()
      console.log("done");
    })
  }
  loadAndSetData();
  setInterval(loadAndSetData, 2000);
})
