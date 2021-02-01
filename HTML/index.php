
<html>
<head>
	 <link rel='stylesheet' href='CSS/graph.css'>
	 <script>
		function Line(str)
		{
			if(str=="Line On")
			{
				var update = {
					mode:"markers"
				};
				Plotly.restyle("Div1", update);
				Plotly.restyle("Div2", update);
				Plotly.restyle("Div3", update);
				Plotly.restyle("Div4", update);

				document.getElementById("vonal").value="Line Off"
			}
			else if(str=="Line Off")
			{
				var update = {
					mode:"lines+markers"
				};
				Plotly.restyle("Div1", update);
				Plotly.restyle("Div2", update);
				Plotly.restyle("Div3", update);
				Plotly.restyle("Div4", update);

				document.getElementById("vonal").value="Line On"
			}
		}
	</script>
</head>

<body>


	<div class = 'intro' id='Div1' ></div>
	<div class = 'intro' id='Div2' ></div>
	<div class = 'intro' id='Div3' ></div>
	<div class = 'intro' id='Div4' ></div>


	<input type='button' name='vonal' id='vonal' value='Line On' onclick='Line(this.value)' />

	<script src='JS/plotly-latest.min.js'></script>
	<?php
	include_once('JS/graph.php');
	?>


</body>
</html>
