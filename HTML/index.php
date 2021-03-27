<?php
	session_start();
?>
<html>
<head>
	<meta charset='utf-8' />
	 <link rel='stylesheet' href='CSS/graph.css'>
	 <script>

	 	var timer = setInterval(myTimer, 1000);
		function myTimer() {
			var xmlhttp = new XMLHttpRequest();
        	xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                eval(this.responseText);
            }
			
        	};
			xmlhttp.open("GET", "JS/graph.php", true);
        	xmlhttp.send();
		}	
	</script>
</head>

<body>
	
	<h1 style="text-align:center;"> Mikó </h1> 
	<iframe src="http://89.46.239.103:8000/player.html" name="restreamer-player" width="800" height="450" scrolling="no" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen="true"></iframe>
	<p id='p1' class = fixed1></p>
	<p id='p2' class = fixed2></p>
	<div id='Div1' ></div>
	<div id='Div2' ></div>
	<div id='Div3' ></div>
	<div id='Div4' ></div>
	<div id='Div5' ></div>
	
	
	
	
	

	<script src='JS/plotly-latest.min.js'></script>
	
	
</body>
</html>
<?php
	session_destroy();
?>
