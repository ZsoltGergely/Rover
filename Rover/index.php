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
	<iframe width="848" height="480" src="https://www.youtube.com/embed/h1Htt--G0u4" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
	<div id='Div1' ></div>
	<div id='Div2' ></div>
	<div id='Div3' ></div>
	<div id='Div4' ></div>
	
	
	
	

	<script src='JS/plotly-latest.min.js'></script>
	
	
</body>
</html>
<?php
	session_destroy();
?>
