const express = require('express');
const app = express();
const port = 8080;

global.data = "This can be accessed anywhere!";

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}


function get_data()
{
    data = '' + getRandomInt(100)

}

// Data can be requested via GET method
app.get('/api', (req, res) => {
    res.json({ text: `${data}` });
});

// You can render page here...

app.listen(port, () => console.log(`Listening on port ${port}`));

while (true)
{
setTimeout(get_data  , 3000);

}
