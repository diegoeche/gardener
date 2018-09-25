function loadData() {
  var url = "/api/plants";
  return $.get(url)
}

$(function () {
  var loadAndSetData = function () {
    $.when(
      loadData(),
    ).done(function (data) {
      data.forEach(function (plant, i) {
        var datasetTemplate = {
          labels: plant.sensors.ma,
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
        }
        var ctx = document.getElementById('canvas-' + plant.id).getContext('2d');
        var config = {
          type: 'bar',
          data: {
            labels: plant.sensors.map((x) => x.name),
            datasets: [datasetTemplate],
          },
          options: {
            responsive: true,
            title: {
              display: true,
              text: plant.name
            },
            legend: {
              display: false
            }
          }
        };
        var chart = new Chart(ctx, config);
        console.log(plant);
        var sensorData = plant.sensors.map(function (sensor) {
          return {
	    "x": sensor.name,
	    "y": sensor.value
          };
        });

        var dataset = chart.data.datasets[0];
        // dataset.label = plant.name;
        // chart.labels = data.map((x) => x.name)
        dataset.labels = plant.sensors.map((x) => x.name)

        // dataset.stack = "stack - " + plant.id + "-"
        dataset.data = [];

        sensorData.forEach((element) => dataset.data.push(element))
        chart.update()
        console.log("done");
      });
    })
  }
  loadAndSetData();
  // setInterval(loadAndSetData, 2000);
})
