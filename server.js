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
      console.log('err ' + JSON.stringify(args) + ' - ' + JSON.stringify(data.toString()));
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

function add_family_member(username, password, fullName, phoneNumber, cb) {
  promisePythonSpawn(['scripts/add_family_member.py', username, password, fullName, phoneNumber]).then((success) => { cb(success.toString()); }).catch((err) => { cb(err.toString()); });
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
  promisePythonSpawn(['scripts/check_login.py', userpass.username, userpass.password]).then((user) => { done(null, JSON.parse(user.toString())); }).catch((err) => { done(err, null); });
  
});


var app = express();

app.use(express.static('HackRPI2019'));


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:false}));

app.use(session({ secret: 'mxsoidjk', resave: false, saveUninitialized: false }));

app.use(passport.initialize());
app.use(passport.session());


//app.use(/\/((?!(login|register)).)*/, (req, res, next) => {
const authMid = (req, res, next) => {
  console.log('auth');
  console.dir(req.user);
  if (!req.user) {
    //res.redirect('/login.html');
    res.status(401).end();
  } else {
    next();
  }
};


app.post('/locationUpdate', authMid, (req, res) => {
  const data = JSON.stringify(req.body.location);
  const username = req.user.username;
  const password = req.user.password;
  console.log("got loc " + username + " " + data);
  promisePythonSpawn(['scripts/save_last_location.py', username, password, data]).then((success) => { res.send(success); }).catch((fail) => { res.send(fail); });
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

//  res.send("gotcha");
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

app.post('/addFamily', authMid, (req, res) => {
  const username = req.user.username;
  const password = req.user.password;
  const fullName = req.body.firstName + " " + req.body.lastName;
  const phoneNumber = req.body.phoneNumber;
  console.log(`addfam ${username} ${password} ${fullName} ${phoneNumber}`);
  
  add_family_member(username, password, fullName, phoneNumber, (result) => { res.send(result); });

  //res.send(result);
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
