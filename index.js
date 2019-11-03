
const { spawn } = require('child_process');

const express = require('express');

const bodyParser = require('body-parser');

var app = express();

app.use(bodyParser.json());

app.use(express.static('public'));

app.get('/', (req, res) => {
  console.log("got get");
  res.render('public/index.html');
});

app.post('/locationUpdate', (req, res) => {
  const data = JSON.stringify(req.body.location);
  const user = "test";
  console.log("got loc " + user + " " + data);
  const sltd = spawn('python3', ["scripts/save_loc_to_db.py", user, data]);
  sltd.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });
  sltd.stderr.on('data', (data) => {
    console.log(`stderr: ${data}`);
  });
  sltd.on('close', (code) => {
    console.log(`close: ${code}`);
  });

  res.send("gotcha");
});



const server = app.listen(8080, '10.150.0.2', () => {
  console.log("listening");
});

async function clean() {
  await server.close();
}

process.on('SIGINT', async () => {
  clean();  
});

process.on('SIGUSR2', async () => {
  clean();
});

process.on('exit', async () => {
  clean();
});
