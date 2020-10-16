// Scripts

_map = document.getElementById('map')
var map = L.map(_map).setView([51.505, -0.09], 4);
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>contributors',
	id: 'mapbox.streets'
}).addTo(map);
L.marker([51.5, -0.09]).addTo(map)
					   .bindPopup('Tweet: some tweet.<br> Suicidal probability: 0.67.')
					   .openPopup();

var ctx = document.getElementById("piechart").getContext("2d");
    var data = {
		labels: ['Suicidal', 'Not Suicidal', 'Neutral'],
		datasets: [{
			data: [10, 4, 6],
			backgroundColor: ["#ff8c82", "#79bbed", "#6dc785"]
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

