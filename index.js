require('dotenv').config()

const { spawn } = require('child_process');

const express = require('express');

const bodyParser = require('body-parser');

const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;

const Cloudant = require('@cloudant/cloudant');

const cloudant = Cloudant({ account: process.env.CLOUDANT_ACCT, plugins: [ { iamauth: { iamApiKey: process.env.CLOUDANT_API_KEY } } ] });
const db = cloudant.db.use('test');


passport.use(new LocalStrategy(
  function (username, password, done) {
    console.log("passport auth " + username + " " + password);
    return done(null, { username, password });
  }
));

passport.serializeUser(function (user, done) {
  done(null, user.uid);
});

passport.deserializeUser(function (uid, done) {
  // find
  done(err, {username: "yes", password: "no"});
});

var app = express();

app.use(express.static('public'));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:false}));

app.use(passport.initialize());
app.use(passport.session());

app.get('/', (req, res) => {
  console.log("got get");
  res.render('public/index.html');
});

app.post('/locationUpdate', (req, res) => {
  const data = JSON.stringify(req.body.location);
  const user = "test";
  console.log("got loc " + user + " " + data);
  //const sltd = spawn('python3', ["scripts/save_loc_to_db.py", user, data]);
  /*sltd.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });
  sltd.stderr.on('data', (data) => {
    console.log(`stderr: ${data}`);
  });
  sltd.on('close', (code) => {
    console.log(`close: ${code}`);
  });*/

  res.send("gotcha");
});

app.post('/login',
  passport.authenticate('local'),
  function (req, res) {
    console.log('login ok ' + req.user.username);
    res.redirect('/');
  }
);

app.post('/register', (req, res) => {
  const username = req.body.username;
  const password = req.body.password;
  console.log("reg user " + username + " " + password);

  // new user

  res.redirect('/');
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
