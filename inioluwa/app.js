var createError = require('http-errors');
var express = require('express');
var path = require('path');
var hbs = require('express-handlebars');

var indexRouter = require('./routes/index');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);


app.listen(1200, function(){
  console.log("server running on port 1200");
});

module.exports = app; //6613 4128