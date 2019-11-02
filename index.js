


const express = require('express');

var app = express();

app.use(express.static('public'));

app.get('/', (req, res) => {
  console.log("got get");
  res.render('public/index.html');
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
