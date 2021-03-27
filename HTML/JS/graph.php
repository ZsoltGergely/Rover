<?php

session_start();

$con=mysqli_connect("exo.xdd.ro","exo","q1w2e3r4t5","exo") or die("adatbazis_hiba");

function datum($str)
{
    $ev = substr($str,0,4);
    $honap = substr($str,5,2);
    $nap = substr($str,8,2);
    $ora = substr($str,11,2);
    $perc = substr($str,14,2);
    $masodperc = substr($str,17,9);
    
    $time = $masodperc + $perc*60 + $ora * 3600 + $nap * 86400;
    return $time;
}

class Graph3D
{
    public $div;
    public $mode;
    public $name;
    public $name0;
    public $name1;
    public $name2;
    public $t0;
    public $t1;
    public $t2;
    public $color;
    public $trace;
    public $data;
    public $layout;
    public $config;

    function __construct($div,$mode,$name,$name0,$name1,$name2,$color)
    {
        $this->div = $div;
        $this->mode = $mode;
        $this->name0=$name0;
        $this->name1= $name1;
        $this->name2= $name2;
        $this->name=$name;
        $this->color = $color;

        #$con=mysqli_connect("exo.xdd.ro","exo","q1w2e3r4t5","exo") or die("adatbazis_hiba");
        global $con; 
        $queryString='select '.$this->name0.','.$this->name1.','.$this->name2.' from sensor_data order by time;';
        $res=mysqli_query($con,$queryString);
        if($res)
        {
            $sor=mysqli_fetch_assoc($res);	  
            $this->t0=$sor[$this->name0];	
            $this->t1=$sor[$this->name1];	
            $this->t2=$sor[$this->name2];

        }
            $this->trace='{
                type: "scatter3d",
                mode:"'.$this->mode.'",
                name:"'.$this->name.'",
                visible: true,
                x:['.$this->t0.'],
                y:['.$this->t1.'],
                z:['.$this->t2.'],
                
                line: {
                width: 2,
                color:"'.$this->color.'",
                },
                marker: {
                size: 3.5,
                color:"'.$this->color.'",
                
                }
                
                }'; 
            $this->data='['.$this->trace.']';
            $updatemenus="[
                {
                    buttons: [
                        {
                            args: ['mode', 'lines+markers'],
                            label: 'Lines+Markers',
                            method: 'restyle'
                        },
                        {
                            args: ['mode', 'markers'],
                            label:'Markers',
                            method:'restyle'
                        },
                        {
                            args: ['mode', 'lines'],
                            label:'Lines',
                            method:'restyle'
                        }
                    ],
                    direction: 'left',
                    pad: {'r': 10, 't': 10},
                    showactive: true,
                    type: 'buttons',
                    x: 0.1,
                    xanchor: 'left',
                    y: 1.1,
                    yanchor: 'top'
                }
            ]";
            $annotations = '[
                {
                text: "Type:",
                showarrow: false,
                align: "left",
                yref: "paper",
                x: 0,
                y: 1.05,
                }
            ]';

            $this->layout ='{
                autosize: false,
                width: 500,
                height: 500,
                updatemenus:'.$updatemenus.',
                annotations:'.$annotations.',
                title: {
                    text:"'.$name.'",
                },
                scene:{
                  xaxis: {
                    title: "'.$name0.'",
                 },
                  yaxis: {
                    title: "'.$name1.'",
                 },
                  zaxis: {
                    title: "'.$name2.'",
                 }},
                margin: {
                l: 0,
                r: 0,
                b: 50,
                t: 100
                }
            }';
            $this->config='{
                responsive: true,
                displaylogo:false
            }';
            echo '
            Plotly.newPlot("'.$div.'",'.$this->data.','.$this->layout.','.$this->config.');
            ';

        if($res)
        {
            while($sor=mysqli_fetch_assoc($res))	
            {

                
                $this->t0=$sor[$this->name0];	
                $this->t1=$sor[$this->name1];	
                $this->t2=$sor[$this->name2];

                if($this->t0!=0 && $this->t1 != 0 && $this->t2 != 0)
                {

                    $data_update = '{
                        x:[['.$this->t0.']],
                        y:[['.$this->t1.']],
                        z:[['.$this->t2.']]  
                    }';
                    echo'
                    Plotly.extendTraces('.$this->div.','.$data_update.',[0]);
                    ';
                }
            }
        }
        
    }
    function Update($x)
    {
        
        #$con=mysqli_connect("exo.xdd.ro","exo","q1w2e3r4t5","exo") or die("adatbazis_hiba");
        global $con;
        if($x>$_SESSION['rowNr'])
        {
            
            $hiany=$x-$_SESSION['rowNr'];
            $queryString='select '.$this->name0.','.$this->name1.','.$this->name2.' from sensor_data order by time desc limit '.$hiany.';';
            $res=mysqli_query($con,$queryString);
            if($res)
            {
                while($sor=mysqli_fetch_assoc($res))	
                {


                    $this->t0=$sor[$this->name0];	
                    $this->t1=$sor[$this->name1];	
                    $this->t2=$sor[$this->name2];

                    if($this->t0!=0 && $this->t1!=0 && $this->t2!=0)
                    {

                        $data_update = '{
                            x:[['.$this->t0.']],
                            y:[['.$this->t1.']],
                            z:[['.$this->t2.']]  
                        }';
                        echo'
                        Plotly.extendTraces('.$this->div.','.$data_update.',[0]);
                        ';
                    }
                }
                    
            }
        }
    }
}

class Graph2D
{
    public $div;
    public $mode;
    public $name0;
    public $name1;
    public $name2;
    public $t0;
    public $t1;
    public $t2;
    public $t_x;
    public $color0;
    public $color1;
    public $color2;
    public $trace0;
    public $trace1;
    public $trace2;
    public $data;
    public $layout;
    public $config;

    function __construct($div,$mode,$name0,$name1,$name2,$color0,$color1,$color2,$m0,$m1,$m2,$time) {
        if($name1=="")
        {
            $this->div = $div;
            $this->mode = $mode;
            $this->name0 = $name0;
            $this->name1 = $name1;
            $this->t0 = 0;
            $this->t_x = 0;
            $this->color0 = $color0;

            #$con=mysqli_connect("exo.xdd.ro","exo","q1w2e3r4t5","exo") or die("adatbazis_hiba");
            global $con;
            $queryString='select '.$this->name0.',time from sensor_data order by time;';
            $res=mysqli_query($con,$queryString);

            if($res)
            {
                $sor=mysqli_fetch_assoc($res);	  
                $this->t0=$sor[$this->name0];
                $this->t_x = datum($sor['time']) - $time; 		
            }

            $this->trace0='{
                type: "scatter",
                mode:"'.$this->mode.'",
                name:"'.$this->name0.'('.$m0.')",
                x:['.$this->t_x.'],
                y:['.$this->t0.'],
                line: {
                width: 1,
                color:"'.$this->color0.'",
                shape: "spline"
                },
                marker: {
                size: 3.5,
                color:"'.$this->color0.'",
                
                }
                
                }';

            $updatemenus="[
                {
                    buttons: [
                        {
                            args: ['mode', 'lines+markers'],
                            label: 'Lines+Markers',
                            method: 'restyle'
                        },
                        {
                            args: ['mode', 'markers'],
                            label:'Markers',
                            method:'restyle'
                        },
                        {
                            args: ['mode', 'lines'],
                            label:'Lines',
                            method:'restyle'
                        }
                    ],
                    direction: 'left',
                    pad: {'r': 10, 't': 10},
                    showactive: true,
                    type: 'buttons',
                    x: 0.1,
                    xanchor: 'left',
                    y: 1.1,
                    yanchor: 'top'
                }
            ]";
            $annotations = '[
                {
                  text: "Type:",
                  showarrow: false,
                  align: "left",
                  yref: "paper",
                  x: 1,
                  y: 1.05,
                }
            ]';
            $this->layout = '{
                autosize: true,
                width: 500,
                height: 500,
                updatemenus:'.$updatemenus.',
                annotations:'.$annotations.',
                margin: {
                l: 50,
                r: 0,
                b: 50,
                t: 150
                },
                xaxis: {
                title:"time(s)",
                range: [0,20]
                },
                yaxis:{
                title:"'.$name0.'('.$m0.')"
                }
            }';
            $this->config='{
                responsive: true,
                displaylogo:false
            }';
            $this->data='['.$this->trace0.']';
            echo '
            Plotly.newPlot("'.$div.'",'.$this->data.','.$this->layout.','.$this->config.');
            ';
            
            if($res)
            {
                    while($sor=mysqli_fetch_assoc($res))	
                {

                        $this->t_x=datum($sor['time'])-$time;
                        $this->t0=$sor[$this->name0];			
                        

                        $data_update = '{
                            y: [['.$this->t0.']],
                            x: [['.$this->t_x.']]
                        }';
                        echo' 
                        Plotly.extendTraces('.$this->div.','.$data_update.',[0]);
                        ';		
                }
                    
            }
        }
        else if($name2=="")
        {
            $this->div = $div;
            $this->mode = $mode;
            $this->name0 = $name0;
            $this->name1 = $name1;
            $this->name2 = $name2;
            $this->t0 = 0;
            $this->t1 = 0;
            $this->t_x = 0;
            $this->color0 = $color0;
            $this->color1 = $color1;

            #$con=mysqli_connect("exo.xdd.ro","exo","q1w2e3r4t5","exo") or die("adatbazis_hiba");
            global $con;
            $queryString='select '.$this->name0.','.$this->name1.',time from sensor_data order by time;';
            $res=mysqli_query($con,$queryString);

            if($res)
            {
                $sor=mysqli_fetch_assoc($res);	  
                $this->t0=$sor[$this->name0];	
                $this->t1=$sor[$this->name1];	
                $this->t_x = datum($sor['time']) - $time; 
            }

            $this->trace0='{
                type: "scatter",
                mode:"'.$this->mode.'",
                name:"'.$this->name0.'('.$m0.')",
                x:['.$this->t_x.'],
                y:['.$this->t0.'],
                line: {
                width: 1,
                color:"'.$this->color0.'",
                shape: "spline"
                },
                marker: {
                size: 3.5,
                color:"'.$this->color0.'",
                
                }
                
                }';

            $this->trace1='{
                type: "scatter",
                mode:"'.$this->mode.'",
                name:"'.$this->name1.'('.$m1.')",
                x:['.$this->t_x.'],
                y:['.$this->t1.'],
                line: {
                    width: 1,
                    color:"'.$this->color1.'",
                    shape: "spline"
                    },
                marker: {
                    size: 3.5,
                    color:"'.$this->color1.'",
                    
                    }
                    
                }';
            $updatemenus="[
                {
                    buttons: [
                        {
                            args: ['mode', 'lines+markers'],
                            label: 'Lines+Markers',
                            method: 'restyle'
                        },
                        {
                            args: ['mode', 'markers'],
                            label:'Markers',
                            method:'restyle'
                        },
                        {
                            args: ['mode', 'lines'],
                            label:'Lines',
                            method:'restyle'
                        }
                    ],
                    direction: 'left',
                    pad: {'r': 10, 't': 10},
                    showactive: true,
                    type: 'buttons',
                    x: 0.1,
                    xanchor: 'left',
                    y: 1.1,
                    yanchor: 'top'
                }
            ]";
            $annotations = '[
                {
                  text: "Type:",
                  showarrow: false,
                  align: "left",
                  yref: "paper",
                  x: 1,
                  y: 1.05,
                }
            ]';
            $this->layout = '{
                autosize: true,
                width: 500,
                height: 500,
                updatemenus:'.$updatemenus.',
                annotations:'.$annotations.',
                margin: {
                l: 50,
                r: 0,
                b: 50,
                t: 150
                },
                xaxis: {
                title:"time(s)",
                range: [0,20]
                }
            }';
            $this->config='{
                responsive: true,
                displaylogo:false
            }';
            $this->data='['.$this->trace0.','.$this->trace1.']';
            echo '
            Plotly.newPlot("'.$div.'",'.$this->data.','.$this->layout.','.$this->config.');
            ';
            
            if($res)
            {
                    while($sor=mysqli_fetch_assoc($res))	
                {

                        $this->t_x = datum($sor['time']) - $time;
                        $this->t0=$sor[$this->name0];	
                        $this->t1=$sor[$this->name1];		
                        

                        $data_update = '{
                            y: [['.$this->t0.'],['.$this->t1.']],
                            x: [['.$this->t_x.'],['.$this->t_x.']]
                        }';
                        echo' 
                        Plotly.extendTraces('.$this->div.','.$data_update.',[0,1]);
                        ';		
                }
                    
            }
        }
        else
        {
            $this->div = $div;
            $this->mode = $mode;
            $this->name0 = $name0;
            $this->name1 = $name1;
            $this->name2 = $name2;
            $this->t0 = 0;
            $this->t1 = 0;
            $this->t2 = 0;
            $this->t_x = 0;
            $this->color0 = $color0;
            $this->color1 = $color1;
            $this->color2 = $color2;

            #$con=mysqli_connect("exo.xdd.ro","exo","q1w2e3r4t5","exo") or die("adatbazis_hiba");
            global $con;
            $queryString='select '.$this->name0.','.$this->name1.','.$this->name2.',time from sensor_data order by time;';
            $res=mysqli_query($con,$queryString);

            if($res)
            {
                $sor=mysqli_fetch_assoc($res);	  
                $this->t0=$sor[$this->name0];	
                $this->t1=$sor[$this->name1];	
                $this->t2=$sor[$this->name2];
                $this->t_x = datum($sor['time']) - $time; 
            }
            

            $this->trace0='{
                type: "scatter",
                mode:"'.$this->mode.'",
                name:"'.$this->name0.'('.$m0.')",
                x:['.$this->t_x.'],
                y:['.$this->t0.'],
                line: {
                width: 1,
                color:"'.$this->color0.'",
                shape: "spline"
                },
                marker: {
                size: 3.5,
                color:"'.$this->color0.'",
                
                }
                
                }';

            $this->trace1='{
                type: "scatter",
                mode:"'.$this->mode.'",
                name:"'.$this->name1.'('.$m1.')",
                x:['.$this->t_x.'],
                y:['.$this->t1.'],
                line: {
                    width: 1,
                    color:"'.$this->color1.'",
                    shape: "spline"
                    },
                marker: {
                    size: 3.5,
                    color:"'.$this->color1.'",
                    
                    }
                    
                }';
            $this->trace2='{
                type: "scatter",
                mode:"'.$this->mode.'",
                name:"'.$this->name2.'('.$m2.')",
                x:['.$this->t_x.'],
                y:['.$this->t2.'],
                line: {
                    width: 1,
                    color:"'.$this->color2.'",
                    shape: "spline"
                    },
                marker: {
                    size: 3.5,
                    color:"'.$this->color2.'",
                    
                    }
                    
                }';
            $this->updatemenus="[
                {
                    buttons: [
                        {
                            args: ['mode', 'lines+markers'],
                            label: 'Lines+Markers',
                            method: 'restyle'
                        },
                        {
                            args: ['mode', 'markers'],
                            label:'Markers',
                            method:'restyle'
                        },
                        {
                            args: ['mode', 'lines'],
                            label:'Lines',
                            method:'restyle'
                        }
                    ],
                    direction: 'left',
                    pad: {'r': 10, 't': 10},
                    showactive: true,
                    type: 'buttons',
                    x: 0.1,
                    xanchor: 'left',
                    y: 1.1,
                    yanchor: 'top'
                }
            ]";
            $annotations = '[
                {
                  text: "Type:",
                  showarrow: false,
                  align: "left",
                  yref: "paper",
                  x: 1,
                  y: 1.05,
                }
            ]';
            $this->layout = '{
                autosize: true,
                width: 500,
                height: 500,
                updatemenus:'.$this->updatemenus.',
                annotations:'.$annotations.',
                margin: {
                l: 50,
                r: 0,
                b: 50,
                t: 150
                },
                xaxis: {
                title:"time(s)",
                range: [0,20]
                }
            }';
            $this->config='{
                responsive: true,
                displaylogo:false
            }';
            $this->data='['.$this->trace0.','.$this->trace1.','.$this->trace2.']';
            echo '
            Plotly.newPlot("'.$div.'",'.$this->data.','.$this->layout.','.$this->config.');
            ';
            
            if($res)
            {
                    while($sor=mysqli_fetch_assoc($res))	
                {

                        $this->t_x = datum($sor['time']) - $time; 
                        $this->t0=$sor[$this->name0];	
                        $this->t1=$sor[$this->name1];	
                        $this->t2=$sor[$this->name2];	
                        

                        $data_update = '{
                            y: [['.$this->t0.'],['.$this->t1.'],['.$this->t2.']],
                            x: [['.$this->t_x.'],['.$this->t_x.'],['.$this->t_x.']]
                        }';
                        echo'
                        Plotly.extendTraces('.$this->div.','.$data_update.',[0,1,2]);
                        ';		
                }
                    
            }
        }
    }
    function Update($x)
    {

        
        #$con=mysqli_connect("exo.xdd.ro","exo","q1w2e3r4t5","exo") or die("adatbazis_hiba");
        global $con;
        if($x>$_SESSION['rowNr'])
        {
            
            if($this->name1=="")
            {
                $hiany=$x-$_SESSION['rowNr'];
                $queryString='select '.$this->name0.',time from sensor_data order by time desc limit '.$hiany.';';
                $res=mysqli_query($con,$queryString);
                if($res)
                {
                    while($sor=mysqli_fetch_assoc($res))	
                    {
                        

                        $this->t_x=datum($sor['time'])-$_SESSION['time0'];
                        $this->t0=$sor[$this->name0];		
                        
                        $data_update = '{
                            y: [['.$this->t0.']],
                            x: [['.$this->t_x.']]
                        }';
                        echo' 
                        Plotly.extendTraces('.$this->div.','.$data_update.',[0]);
                        ';
                        if($this->t_x > 20){
                            $k = $this->t_x - 20;
                            $p = $this->t_x;
                            $relayout = '{
                                xaxis:{
                                    range:['.$k.','.$p.']
                                }
                            }';
                            echo'
                            Plotly.relayout('.$this->div.','.$relayout.');
                            ';
                        }		
                    }
                        
                }

            }
            else if($this->name2=="")
            {
                $hiany=$x-$_SESSION['rowNr'];
                $queryString='select '.$this->name0.','.$this->name1.',time from sensor_data order by time desc limit '.$hiany.';';
                $res=mysqli_query($con,$queryString);
                if($res)
                {
                    while($sor=mysqli_fetch_assoc($res))	
                    {

                        $this->t_x = datum($sor['time'])-$_SESSION['time0']; 
                        $this->t0=$sor[$this->name0];	
                        $this->t1=$sor[$this->name1];		
                        
                        $data_update = '{
                            y: [['.$this->t0.'],['.$this->t1.']],
                            x: [['.$this->t_x.'],['.$this->t_x.']]
                        }';
                        echo' 
                        Plotly.extendTraces('.$this->div.','.$data_update.',[0,1]);
                        ';
                        if($this->t_x > 20){
                            $k = intval($this->t_x - 20);
                            $p = intval($this->t_x);
                            $relayout = '{
                                xaxis:{
                                    range:['.$k.','.$p.']
                                }
                            }';

                            echo'
                            Plotly.relayout('.$this->div.','.$relayout.');
                            ';
                        }		
                    }
                        
                }

            }
            else
            {
                $hiany=$x-$_SESSION['rowNr'];
                $queryString='select '.$this->name0.','.$this->name1.','.$this->name2.',time from sensor_data order by time desc limit '.$hiany.';';
                $res=mysqli_query($con,$queryString);
                if($res)
                {
                    while($sor=mysqli_fetch_assoc($res))	
                    {

                        $this->t_x = datum($sor['time'])-$_SESSION['time0']; 
                        $this->t0=$sor[$this->name0];	
                        $this->t1=$sor[$this->name1];
                        $this->t2=$sor[$this->name2];		
                        
                        $data_update = '{
                            y: [['.$this->t0.'],['.$this->t1.'],['.$this->t2.']],
                            x: [['.$this->t_x.'],['.$this->t_x.'],['.$this->t_x.']]
                        }';
                        echo' 
                        Plotly.extendTraces('.$this->div.','.$data_update.',[0,1,2]);
                        ';
                        
                        if($this->t_x > 20){
                            $k = intval($this->t_x - 20);
                            $p = intval($this->t_x);
                            $relayout = '{
                                xaxis:{
                                    range:['.$k.','.$p.']
                                }
                            }';

                            echo'
                            Plotly.relayout('.$this->div.','.$relayout.');
                            ';
                        }
                    }
                        
                }
            }
        }
    }
}


if (isset($_SESSION['GraphGyro'],$_SESSION['GraphAir'],$_SESSION['GraphLight'],$_SESSION['GraphGas'],$_SESSION['time0']))
{
    #$con=mysqli_connect("exo.xdd.ro","exo","q1w2e3r4t5","exo") or die("adatbazis_hiba");
    global $con; 
    $queryString='select count(*) from sensor_data where 1';
    $res=mysqli_query($con,$queryString);
    $x=mysqli_fetch_assoc($res);
    
    $_SESSION['GraphSpeed']->Update($x['count(*)']);
    $_SESSION['GraphGas']->Update($x['count(*)']);
    $_SESSION['GraphAir']->Update($x['count(*)']);
    $_SESSION['GraphLight']->Update($x['count(*)']);
    $_SESSION['GraphGyro']->Update($x['count(*)']);

    

    $_SESSION['rowNr']=$x['count(*)'];

    
    
    
}
else
{
    $queryString='select min(time) from sensor_data';
    $res=mysqli_query($con,$queryString);
    $x=mysqli_fetch_assoc($res);
    echo'
        document.getElementById("p1").innerHTML = "First data arrived at: ";
        document.getElementById("p2").innerHTML = "'.$x['min(time)']. '";
    ';
    $time0 = datum($x['min(time)']);
    if($x['min(time)']!="")
    {
        $_SESSION['time0']=$time0;
    }

    $GraphGyro = new Graph3D('Div1','lines+markers','GPS','latitude','longitude','altitude',"red");
    $GraphAir = new Graph2D('Div2','lines+markers','pressure','temperature','humidity','red','green','blue',"kPa","°C","%",$time0);
    $GraphLight = new Graph2D('Div3','lines+markers','uv_index','ir_light','visible_light','red','green','blue',"25 mW/m²","25 mW/m²","25 mW/m²",$time0);
    $GraphGas = new Graph2D('Div4','lines+markers','eco2','tvoc','','red','green','',"ppm","ppm","",$time0);
    $GraphSpeed = new Graph2D('Div5','lines+markers','speed','','','red','','','m/s','','',$time0);
    $_SESSION['GraphGyro']=$GraphGyro;
    $_SESSION['GraphAir']=$GraphAir;
    $_SESSION['GraphLight']=$GraphLight;
    $_SESSION['GraphGas']=$GraphGas;
    $_SESSION['GraphSpeed']=$GraphSpeed;

    #$con=mysqli_connect("exo.xdd.ro","exo","q1w2e3r4t5","exo") or die("adatbazis_hiba");
    $queryString='select count(*) from sensor_data where 1';
    $res=mysqli_query($con,$queryString);
    $x=mysqli_fetch_assoc($res);
    $_SESSION['rowNr']=$x['count(*)'];
    
}


?>