// Scripts

// Modal
var modal = document.getElementById('id01');
	
window.onclick = function(event) {
	if (event.target == modal) {
		modal.style.display = 1; //"none";
	}
}

/*/ Map
_map = document.getElementById('map')
var map = L.map(_map).setView([51.505, -0.09], 4);
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>contributors',
	id: 'mapbox.streets'
}).addTo(map);
L.marker([51.5, -0.09]).addTo(map)
					   .bindPopup('Tweet: some tweet.<br> Suicidal probability: 0.67.')
					   .openPopup();
*/

// Doughnut chart
var ctx = document.getElementById("piechart").getContext("2d");
var data = {
	labels: ['Suicidal', 'Not Suicidal', 'Neutral'],
	datasets: [{
		data: data_.counts, //[sl, nsl, ntl],
		backgroundColor: ["#ff8c82", "#6dc785", "#79bbed"]
	}]
}
var myDoughnutChart = new Chart(ctx, {
type: 'doughnut',
data: data,
options: {
	responsive: true,
	legend:{
		display: true,
		position: 'right',
		labels: {usePointStyle: true},
	},
}
});

// Bar chart
var bar_chart = document.getElementById("barchart").getContext("2d");

var myBarChart = new Chart(bar_chart, {
	type: 'horizontalBar',
	data: {
	  labels: ["Suicidal", "Non Suicidal", "Neutral"],
	  datasets: [{
		  categoryPercentage: 1.0,
		  barPercentage: 1.0,
		  //barThickness: 3,
		  data: data_.counts, //[72, 16, 9],
		  backgroundColor: ["#ff8c82", "#6dc785", "#79bbed"]

	  }]
	},
	options: {
	  legend: {
		display: false,
		position: 'right',
		labels: {usePointStyle: true},
	  },
	  scales: {
		xAxes: [{
		  display: true,
		  //beginAtZero: true,
		  //ticks: {
			//  min: 0,
		  //}
		}],
		yAxes: [{
			display: false,
			beginAtZero: true,
		}],
	  }
	}
  });


// Line Chart
var l_chart = document.getElementById("linechart").getContext("2d");
var line_data = {
	//labels: ['M', 'T', 'W', 'T', 'F', 'S', 'S'],
	datasets: [{
		label: 'Suicidal',
		data: [0, data_.counts[0]], //[12, 19, 3, 17, 6, 3, 7],
		backgroundColor: "#ff8c82"
	}, {
		label: 'Non Suicidal',
		data: [0, data_.counts[1]], //[2, 29, 5, 5, 2, 3, 10],
		backgroundColor: "#6dc785"
	},
	{
		label: 'Neutral',
		data: [[0],data_.counts[2]],//[2, 19, 5, 5, 2, 3, 10],
		backgroundColor: "#c6e0f7"
	}]
	};

var myLineChart = Chart.Line(l_chart,{
	data:line_data,
	options:{
		responsive: true,
		legend:{
			display: true,
			position: 'right',
			labels: {usePointStyle: true},
			},
			scales: {
				yAxes:[{
					stacked:true,
					gridLines: {
						display:true,
						color:"rgba(255,99,132,0.2)"
						}
						}],
				xAxes:[{
					gridLines: {
						display:true
						}
						}]
					}
			}
		});

// Line Chart test
var l1_chart = document.getElementById("linechart1").getContext("2d");
var l_data = {
	labels: ['0', '1', '2', '3', '4', '5', '6'],
	datasets: [{
		label: 'Suicidal',
		data: [12, 19, 3, 17, 6, 3, 7], //timeseries.suicidal,
		backgroundColor: "#ff8c82"
	}, {
		label: 'Non Suicidal',
		data: [2, 13, 5, 1, 6, 3, 12], //timeseries.non_suicidal,
		backgroundColor: "#6dc785"
	},
	{
		label: 'Neutral',
		data: [2, 19, 5, , 2, 3, 10], //timeseries.neutral,
		backgroundColor: "#c6e0f7"
	}]
	};

var myLineChart = Chart.Line(l1_chart,{
	data:l_data,
	options:{
		responsive: true,
		legend:{
			display: true,
			position: 'right',
			labels: {usePointStyle: true},
			},
			scales: {
				yAxes:[{
					stacked:true,
					gridLines: {
						display:true,
						color:"rgba(255,99,132,0.2)"
						}
						}],
				xAxes:[{
					gridLines: {
						display:true
						}
						}]
					}
			}
		});
