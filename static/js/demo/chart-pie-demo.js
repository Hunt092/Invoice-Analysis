// Set new default font family and font color to mimic Bootstrap's default styling
(Chart.defaults.global.defaultFontFamily = "Nunito"),
	'-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = "#858796";

function getRandomColor() {
	var letters = "0123456789ABCDEF";
	var color = "#";
	for (var i = 0; i < 6; i++) {
		color += letters[Math.floor(Math.random() * 16)];
	}
	return color;
}

fetch("/vendor_total")
	.then((response) => response.json())
	.then((data) => {
		// Do something with the data
		BackgroundColors = [];
		data.vendor_name.forEach((vendor) => {
			BackgroundColors.push(getRandomColor());
		});
		var ctx = document.getElementById("myPieChart");
		var myPieChart = new Chart(ctx, {
			type: "doughnut",
			data: {
				labels: data.vendor_name,
				datasets: [
					{
						data: data.total_amount,
						backgroundColor: BackgroundColors,
						hoverBackgroundColor: ["#2e59d9", "#17a673", "#2c9faf"],
						hoverBorderColor: "rgba(234, 236, 244, 1)",
					},
				],
			},
			options: {
				maintainAspectRatio: false,
				tooltips: {
					backgroundColor: "rgb(255,255,255)",
					bodyFontColor: "#858796",
					borderColor: "#dddfeb",
					borderWidth: 1,
					xPadding: 15,
					yPadding: 15,
					displayColors: false,
					caretPadding: 10,
				},
				legend: {
					display: false,
				},
				cutoutPercentage: 80,
			},
		});
	})
	.catch((error) => {
		// Handle any errors
		console.error(error);
	});

// Pie Chart Example
