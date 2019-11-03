require('dotenv').config()

const { spawn } = require('child_process');

function promisePythonSpawn(args) {
  cp = spawn('python3', args);
  return new Promise((res, rej) => {
    cp.stdout.on('data', (data) => {
      console.log('out ' + JSON.stringify(args) + ' - ' + JSON.stringify(data));
      res(data);
    });
    cp.stderr.on('data', (data) => {
      console.log('err ' + JSON.stringify(args) + ' - ' + JSON.stringify(data));
      rej(data);
    });
    /*
    cp.on('close', (code) => {
      console.log('close ' + JSON.stringify(args) + ' - ' + JSON.stringify(args));
      if (code == 0) {
        res(null);
      } else {
        rej(null);
      }
    });*/
  });
}

function check_login(username, password) {
  promisePythonSpawn(['scripts/check_login.py', username, password]).then((user) => { return JSON.parse(user.toString()); }).catch((err) => { console.error(err.toString()); return null; });
}

function create_user(username, password) {
  promisePythonSpawn(['scripts/create_new_user.py', username, password]);
}
  

const express = require('express');

const session = require('express-session');

const bodyParser = require('body-parser');

const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;


passport.use(new LocalStrategy(
  function (username, password, done) {
    console.log("passport auth " + username + " " + password);
    promisePythonSpawn(['scripts/check_login.py', username, password]).then((user) => { done(null, JSON.parse(user.toString())); }).catch((err) => { done(null, false, { message: err.toString() }); });
  }
));

passport.serializeUser(function (user, done) {
  console.log("ser " + JSON.stringify(user));
  done(null, {username:user.username, password:user.password});
});

passport.deserializeUser(function (userpass, done) {
  // find
  console.log("des " + JSON.stringify(userpass));
  promisePythonSpawn(['scripts/check_login.py', userpass.username, userpass.password]).then((user) => { done(null, user); }).catch((err) => { done(err, null); });
  
});


var app = express();

//app.use(express.static('public'));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:false}));

app.use(session({ secret: 'mxsoidjk' }));

app.use(passport.initialize());
app.use(passport.session());


app.use(/\/((?!(login|register)).)*/, (req, res, next) => {
  console.log('auth');
  console.dir(req.user);
  if (!req.user) {
    res.redirect('/login.html');
  } else {
    next();
  }
});


app.use(express.static('HackRPI2019'));


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
  create_user(username, password);

  res.redirect('/');
});



const server = app.listen(8080, () => {
// const server = app.listen(8080, '10.150.0.2', () => {
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
