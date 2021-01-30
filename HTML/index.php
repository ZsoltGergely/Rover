<?php
echo "
<html>
<head>
	 <link rel='stylesheet' href='../CSS/graph.css'>
</head>

<body>


	<div class = 'intro' id='Div2D' ></div>
	<div class = 'intro' id='Div3D' ></div>
	<div class = 'intro' id='MyDiv' ></div>


	<input type=button onclick='Line()' id='vonal' value='Line On' />


	<script src='JS/plotly-latest.min.js'></script> ";
	include_once('JS/graph.php');

	"
</body>
</html>
"
?>
