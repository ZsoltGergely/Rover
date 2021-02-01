<?php

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

        $con=mysqli_connect("exo.xdd.ro","user","pass","exo") or die("adatbazis_hiba");
        $queryString='select '.$this->name0.','.$this->name1.','.$this->name2.' from sensor_data limit 10;';
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

        $this->layout ='{
            autosize: false,
            width: 500,
            height: 500,
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
        echo '<script>
        Plotly.newPlot("'.$div.'",'.$this->data.','.$this->layout.','.$this->config.');
        </script> ';

        if($res)
        {
            while($sor=mysqli_fetch_assoc($res))
            {

                $this->t0=$sor[$this->name0];
                $this->t1=$sor[$this->name1];
                $this->t2=$sor[$this->name2];

            $data_update = '{
                x:[['.$this->t0.']],
                y:[['.$this->t1.']],
                z:[['.$this->t2.']]
            }';
            echo'
            <script>
            Plotly.extendTraces('.$this->div.','.$data_update.',[0])
            </script>';
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

    function __construct($div,$mode,$name0,$name1,$name2,$color0,$color1,$color2) {
        if($name2=="")
        {
            $this->div = $div;
            $this->mode = $mode;
            $this->name0 = $name0;
            $this->name1 = $name1;
            $this->t0 = 0;
            $this->t1 = 0;
            $this->t_x = 0;
            $this->color0 = $color0;
            $this->color1 = $color1;

            $con=mysqli_connect("exo.xdd.ro","user","pass","exo") or die("adatbazis_hiba");
            $queryString='select '.$this->name0.','.$this->name1.' from sensor_data limit 10;';
            $res=mysqli_query($con,$queryString);

            if($res)
            {
                $sor=mysqli_fetch_assoc($res);
                $this->t0=$sor[$this->name0];
                $this->t1=$sor[$this->name1];
            }

            $this->trace0='{
                type: "scatter",
                mode:"'.$this->mode.'",
                name:"'.$this->name0.'",
                x:['.$this->t_x.'],
                y:['.$this->t0.'],
                line: {
                width: 1,
                color:"'.$this->color0.'",
                },
                marker: {
                size: 3.5,
                color:"'.$this->color0.'",

                }

                }';

            $this->trace1='{
                type: "scatter",
                mode:"'.$this->mode.'",
                name:"'.$this->name1.'",
                x:['.$this->t_x.'],
                y:['.$this->t1.'],
                line: {
                    width: 1,
                    color:"'.$this->color1.'",
                    },
                marker: {
                    size: 3.5,
                    color:"'.$this->color1.'",

                    }

                }';
            $this->layout = '{
                autosize: false,
                width: 500,
                height: 500,
                margin: {
                l: 50,
                r: 0,
                b: 50,
                t: 150
                },
                yaxis: {
                range: [0,100]
                }
            }';
            $this->config='{
                responsive: true,
                displaylogo:false
            }';
            $this->data='['.$this->trace0.','.$this->trace1.']';
            echo '<script>
            Plotly.newPlot("'.$div.'",'.$this->data.','.$this->layout.','.$this->config.');
            </script>';

            if($res)
            {
                    while($sor=mysqli_fetch_assoc($res))
                {

                        $this->t_x++;
                        $this->t0=$sor[$this->name0];
                        $this->t1=$sor[$this->name1];


                        $data_update = '{
                            y: [['.$this->t0.'],['.$this->t1.']],
                            x: [['.$this->t_x.'],['.$this->t_x.']]
                        }';
                        echo' <script>
                        Plotly.extendTraces('.$this->div.','.$data_update.',[0,1])
                        </script>';
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

            $con=mysqli_connect("exo.xdd.ro","user","pass","exo") or die("adatbazis_hiba");
            $queryString='select '.$this->name0.','.$this->name1.','.$this->name2.' from sensor_data limit 10;';
            $res=mysqli_query($con,$queryString);

            if($res)
            {
                $sor=mysqli_fetch_assoc($res);
                $this->t0=$sor[$this->name0];
                $this->t1=$sor[$this->name1];
                $this->t2=$sor[$this->name2];
            }


            $this->trace0='{
                type: "scatter",
                mode:"'.$this->mode.'",
                name:"'.$this->name0.'",
                x:['.$this->t_x.'],
                y:['.$this->t0.'],
                line: {
                width: 1,
                color:"'.$this->color0.'",
                },
                marker: {
                size: 3.5,
                color:"'.$this->color0.'",

                }

                }';

            $this->trace1='{
                type: "scatter",
                mode:"'.$this->mode.'",
                name:"'.$this->name1.'",
                x:['.$this->t_x.'],
                y:['.$this->t1.'],
                line: {
                    width: 1,
                    color:"'.$this->color1.'",
                    },
                marker: {
                    size: 3.5,
                    color:"'.$this->color1.'",

                    }

                }';
            $this->trace2='{
                type: "scatter",
                mode:"'.$this->mode.'",
                name:"'.$this->name2.'",
                x:['.$this->t_x.'],
                y:['.$this->t2.'],
                line: {
                    width: 1,
                    color:"'.$this->color2.'",
                    },
                marker: {
                    size: 3.5,
                    color:"'.$this->color2.'",

                    }

                }';
            $this->layout = '{
                autosize: false,
                width: 500,
                height: 500,
                margin: {
                l: 50,
                r: 0,
                b: 50,
                t: 150
                },
                yaxis: {
                range: [0,100]
                }
            }';
            $this->config='{
                responsive: true,
                displaylogo:false
            }';
            $this->data='['.$this->trace0.','.$this->trace1.','.$this->trace2.']';
            echo '<script>
            Plotly.newPlot("'.$div.'",'.$this->data.','.$this->layout.','.$this->config.');
            </script>';

            if($res)
            {
                    while($sor=mysqli_fetch_assoc($res))
                {

                        $this->t_x++;
                        $this->t0=$sor[$this->name0];
                        $this->t1=$sor[$this->name1];
                        $this->t2=$sor[$this->name2];


                        $data_update = '{
                            y: [['.$this->t0.'],['.$this->t1.'],['.$this->t2.']],
                            x: [['.$this->t_x.'],['.$this->t_x.'],['.$this->t_x.']]
                        }';
                        echo' <script>
                        Plotly.extendTraces('.$this->div.','.$data_update.',[0,1,2])
                        </script>';
                }

            }
        }
    }
      function Line()
      {
          if($this->mode=='lines+markers')
          {
            $this->mode='markers';
          }
          else if($this->mode=='markers')
          {
            $this->mode='lines+markers';
          }
          $update='{
              mode:"'.$this->mode.'"
          }';
          echo'<script>
          Plotly.restyle("'.$this->div.'",'.$update.');
          </script>';
      }
}


$GraphGyro = new Graph3D('Div1','lines+markers','Gyro','gyro_x','gyro_y','gyro_z',"red");
$GraphAir = new Graph2D('Div2','lines+markers','presssure','temperature','humidity','red','green','blue');
$GraphLight = new Graph2D('Div3','lines+markers','uv_index','ir_light','visible_light','red','green','blue');
$GraphGas = new Graph2D('Div4','lines+markers','eco2','tvoc','','red','green','');


?>
