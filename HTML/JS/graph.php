<?php


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
function data($t)
{
    $str = "";
    for($i=0;$i<count($t);$i++)
    {
        $str =$str.$t[$i].", ";
    }
    $str = substr($str,0,strlen($str)-2);
    return $str;
}

class Graph2D
{
    public $div;
    public $mode;
    public $name0;
    public $name1;
    public $name2;
    public $name3;
    public $t0;
    public $t1;
    public $t2;
    public $t3;
    public $t_x ;
    public $color0;
    public $color1;
    public $color2;
    public $color3;
    public $trace0;
    public $trace1;
    public $trace2;
    public $trace3;
    public $data;
    public $layout;
    public $config;

    function __construct($div,$mode,$name0,$name1,$name2,$name3,$color0,$color1,$color2,$color3,$m0,$m1,$m2,$m3,$time,$table) {
            
            $this->div = $div;
            $this->mode = $mode;
            $this->name0 = $name0;
            $this->name1 = $name1;
            $this->name2 = $name2;
            $this->name3 = $name3;
            $tmpx = array();
            $tmp0 =array();
            $tmp1 = array();
            $tmp2 = array();
            $tmp3 = array();
            $this->color0 = $color0;
            $this->color1 = $color1;
            $this->color2 = $color2;
            $this->color3 = $color3;

            #$con=mysqli_connect("exo.xdd.ro","exo","q1w2e3r4t5","exo") or die("adatbazis_hiba");
            global $con;
            $queryString='select '.$this->name0.','.$this->name1.','.$this->name2.','.$this->name3.',time from '.$table.' order by time;';
            $res=mysqli_query($con,$queryString);

            if($res)
            {
                while($sor=mysqli_fetch_assoc($res))	
                {
                    array_push($tmpx,datum($sor['time'])-$time);
                    array_push($tmp0,$sor[$this->name0]);	
                    array_push($tmp1,$sor[$this->name1]);
                    array_push($tmp2,$sor[$this->name2]);
                    array_push($tmp3,$sor[$this->name3]);
                }
            }
            $this->t_x=data($tmpx);
            $this->t0=data($tmp0);
            $this->t1=data($tmp1);
            $this->t2=data($tmp2);
            $this->t3=data($tmp3);

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
                size: 2,
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
                    size: 2,
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
                    size: 2,
                    color:"'.$this->color2.'",
                    
                    }
                    
                }';
            $this->trace3='{
                type: "scatter",
                mode:"'.$this->mode.'",
                name:"'.$this->name3.'('.$m3.')",
                x:['.$this->t_x.'],
                y:['.$this->t3.'],
                line: {
                    width: 1,
                    color:"'.$this->color3.'",
                    shape: "spline"
                    },
                marker: {
                    size: 2,
                    color:"'.$this->color3.'",
                    
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
                width: 1400,
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
                }
            }';
            $this->config='{
                responsive: true,
                displaylogo:false
            }';
            $this->data='['.$this->trace0.','.$this->trace1.','.$this->trace2.','.$this->trace3.']';
            echo '
            Plotly.newPlot("'.$div.'",'.$this->data.','.$this->layout.','.$this->config.');
            ';
    }
}

$M = array(
    "pressure"=>"kPa",
    "temperature"=>"°C",
    "humidity"=>"%",
    "gyro_x"=>"dps",
    "gyro_y"=>"dps",
    "gyro_z"=>"dps",
    "uv_index"=>"index",
    "ir_light"=>"index",
    "visible_light"=>"index",
    "eco2"=>"ppm",
    "tvoc"=>"ppm",
    "rawh2"=>"ppm",
    "rawhethanol"=>"ppm",
    "acc_x"=>"g",
    "acc_y"=>"g",
    "acc_z"=>"g",
    "mag_x"=>"mT",
    "mag_y"=>"mT",
    "mag_z"=>"mT",
    "latitude"=>"decimal degrees",
    "longitude"=>"decimal degrees",
    "altitude"=>"m",
    "speed"=>"m/s",
    "acc"=>"g",
    "gyro"=>"dps",
    "mag"=>"mT"
    

);
$data1 = $_REQUEST["data1"];
$data2 = $_REQUEST["data2"];
$data3 = $_REQUEST["data3"];
$data3 = $_REQUEST["data4"];

$queryString='select min(time) from sensor_data_01';
$res=mysqli_query($con,$queryString);
$x=mysqli_fetch_assoc($res);
echo'
    document.getElementById("p01").innerHTML = "First measurement:";
    document.getElementById("p1").innerHTML = "First data arrived at: '.$x['min(time)'].' ";
';
$time0 = datum($x['min(time)']);

$Graph = new Graph2D('Div1','lines+markers',$_REQUEST["data1"],$_REQUEST["data2"],$_REQUEST["data3"],$_REQUEST["data4"],'red','green','blue','purple',$M[$_REQUEST["data1"]],$M[$_REQUEST["data2"]],$M[$_REQUEST["data3"]],$M[$_REQUEST["data4"]],$time0,"sensor_data_01");
$queryString='select min(time) from sensor_data_2';
$res=mysqli_query($con,$queryString);
$x=mysqli_fetch_assoc($res);
echo'
    document.getElementById("p02").innerHTML = "Second measurement:";
    document.getElementById("p2").innerHTML = "First data arrived at: '.$x['min(time)'].' ";
';
$time0 = datum($x['min(time)']);
$Graph = new Graph2D('Div2','lines+markers',$_REQUEST["data1"],$_REQUEST["data2"],$_REQUEST["data3"],$_REQUEST["data4"],'red','green','blue','purple',$M[$_REQUEST["data1"]],$M[$_REQUEST["data2"]],$M[$_REQUEST["data3"]],$M[$_REQUEST["data4"]],$time0,"sensor_data_2");

?>