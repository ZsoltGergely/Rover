<html>
<head>
	<meta charset='utf-8' />
	<link rel="stylesheet" href="CSS/graph.css">
</head>

<body>
	
	<h1 style="text-align:center;"> Mikó </h1> 
	<p><a href="https://www.youtube.com/watch?v=pmE20V8H2Y4&list=PLNS3aSu6iQAVwH8XDAT-jYIKXt3ivJpmy">You can rewatch our stream HERE!</a></p>

	<form method = "post">
  	<label for="fname">Trace1:</label>
  	<select name="data1" id="data1">
		<option value="pressure">pressure</option>
		<option value="temperature">temperature</option>
		<option value="humidity">humidity</option>
		<option value="gyro_x">gyroscope_x</option>
		<option value="gyro_y">gyroscope_y</option>
		<option value="gyro_z">gyroscope_z</option>
		<option value="uv_index">uv_index</option>
		<option value="ir_light">ir_light</option>
		<option value="visible_light">visible_light</option>
		<option value="eco2">eco2</option>
		<option value="tvoc">tvoc</option>
		<option value="acc_x">acceleration_x</option>
		<option value="acc_y">acceleration_y</option>
		<option value="acc_z">acceleration_z</option>
		<option value="mag_x">magnetometer_x</option>
		<option value="mag_y">magnetometer_y</option>
		<option value="mag_z">magnetometer_z</option>
		<option value="latitude">latitude</option>
		<option value="longitude">longitude</option>
		<option value="altitude">altitude</option>
		<option value="speed">speed</option>
		<option value="acc">acceleration</option>
		<option value="gyro">gyroscope</option>
		<option value="mag">magnetometer</option>

		
	</select>

	<label for="fname">Trace2:</label>
  	<select name="data2" id="data2">
		<option value="pressure">pressure</option>
		<option value="temperature">temperature</option>
		<option value="humidity">humidity</option>
		<option value="gyro_x">gyroscope_x</option>
		<option value="gyro_y">gyroscope_y</option>
		<option value="gyro_z">gyroscope_z</option>
		<option value="uv_index">uv_index</option>
		<option value="ir_light">ir_light</option>
		<option value="visible_light">visible_light</option>
		<option value="eco2">eco2</option>
		<option value="tvoc">tvoc</option>
		<option value="acc_x">acceleration_x</option>
		<option value="acc_y">acceleration_y</option>
		<option value="acc_z">acceleration_z</option>
		<option value="mag_x">magnetometer_x</option>
		<option value="mag_y">magnetometer_y</option>
		<option value="mag_z">magnetometer_z</option>
		<option value="latitude">latitude</option>
		<option value="longitude">longitude</option>
		<option value="altitude">altitude</option>
		<option value="speed">speed</option>
		<option value="acc">acceleration</option>
		<option value="gyro">gyroscope</option>
		<option value="mag">magnetometer</option>

		
	</select>

	<label for="fname">Trace3:</label>
  	<select name="data3" id="data3">
		<option value="pressure">pressure</option>
		<option value="temperature">temperature</option>
		<option value="humidity">humidity</option>
		<option value="gyro_x">gyroscope_x</option>
		<option value="gyro_y">gyroscope_y</option>
		<option value="gyro_z">gyroscope_z</option>
		<option value="uv_index">uv_index</option>
		<option value="ir_light">ir_light</option>
		<option value="visible_light">visible_light</option>
		<option value="eco2">eco2</option>
		<option value="tvoc">tvoc</option>
		<option value="acc_x">acceleration_x</option>
		<option value="acc_y">acceleration_y</option>
		<option value="acc_z">acceleration_z</option>
		<option value="mag_x">magnetometer_x</option>
		<option value="mag_y">magnetometer_y</option>
		<option value="mag_z">magnetometer_z</option>
		<option value="latitude">latitude</option>
		<option value="longitude">longitude</option>
		<option value="altitude">altitude</option>
		<option value="speed">speed</option>
		<option value="acc">acceleration</option>
		<option value="gyro">gyroscope</option>
		<option value="mag">magnetometer</option>

		
	</select>

	<label for="fname">Trace4:</label>
  	<select name="data4" id="data4">
		<option value="pressure">pressure</option>
		<option value="temperature">temperature</option>
		<option value="humidity">humidity</option>
		<option value="gyro_x">gyroscope_x</option>
		<option value="gyro_y">gyroscope_y</option>
		<option value="gyro_z">gyroscope_z</option>
		<option value="uv_index">uv_index</option>
		<option value="ir_light">ir_light</option>
		<option value="visible_light">visible_light</option>
		<option value="eco2">eco2</option>
		<option value="tvoc">tvoc</option>
		<option value="acc_x">acceleration_x</option>
		<option value="acc_y">acceleration_y</option>
		<option value="acc_z">acceleration_z</option>
		<option value="mag_x">magnetometer_x</option>
		<option value="mag_y">magnetometer_y</option>
		<option value="mag_z">magnetometer_z</option>
		<option value="latitude">latitude</option>
		<option value="longitude">longitude</option>
		<option value="altitude">altitude</option>
		<option value="speed">speed</option>
		<option value="acc">acceleration</option>
		<option value="gyro">gyroscope</option>
		<option value="mag">magnetometer</option>

		
	</select>
	<input type="submit" value=Submit>
	</form>
	<h2 id='p01' style="text-align:center"></h2>
	<p id='p1'></p>
	<div id='Div1' ></div>
	<h2 id='p02' style="text-align:center"></h2>
	<p id='p2'></p>
	<div id='Div2' ></div>
	<script src='JS/plotly-latest.min.js'></script>
	<?php
	if(isset($_REQUEST["data1"],$_REQUEST["data2"],$_REQUEST["data3"],$_REQUEST["data4"]))
	{
		echo '
		<script>
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				eval(this.responseText);
			}
			};
			xmlhttp.open("GET", "JS/graph.php?data1='.$_REQUEST["data1"].'&data2='.$_REQUEST["data2"].'&data3='.$_REQUEST["data3"].'&data4='.$_REQUEST["data4"].'", true);
			xmlhttp.send();
		</script>
		';
	}
	?>
	
</body>
</html>