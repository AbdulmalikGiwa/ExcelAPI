var express = require('express');
var router = express.Router();
const { check, validationResult } = require('express-validator/check');

router.get('/', function(req, res, next) {
  res.render('index', {layout: false});
});

router.post('/', function(req, res, next) {
  // putting value from from into contaniers
  var name = req.body.name;
  console.log(name);
  var street_address = req.body.street_address;
  var city = req.body.city;
  var state = req.body.state;
  var zip = req.body.zip;
  var username = req.body.username;
  var email = req.body.email;
  var password = req.body.password;
  var password2 = req.body.password2;
  var ipAddress = req.connection.address();
  console.log(`${name} ${street_address} ${password}`)

  // form validation
  check('name', 'min character 4 and max character 30')
    .not()
    .isEmpty()
    .isLength({
      min: 4,
      max: 30
    }).matches(/[^a-zA-Z]/g);
  check('street_address', 'min character 4 and max character 35')
    .not()
    .isEmpty()
    .isLength({
      min: 4,
      max: 35
    }).matches(/[^a-zA-Z0-9]/g);
  check('city', 'min character 3 and max character 20')
    .not()
    .isEmpty()
    .isLength({
      min: 3,
      max: 20
    }).matches(/[^a-zA-Z]/g);
  check('state', 'min character 3 and max character 20')
    .not()
    .isEmpty()
    .isLength({
      min: 3,
      max: 20
    }).matches(/[^a-zA-Z]/g);
  check('zip', 'Input Valid Zip Code')
    .not()
    .isEmpty()
    .isInt()
    .isLength({
      min: 4,
      max: 6
    });
  check('email', 'min character 6 and max character 35')
    .not()
    .isEmpty()
    .isLength({
      min: 6,
      max: 35
    });
  check('email', 'Email not valid').isEmail().normalizeEmail().custom((value, {req}) => {
    return new Promise((resolve, reject) => {
      // dns check email
      dns_validate_email.validEmail(value, (valid) => {
        console.log(`valid: ${vali}`);
        if (valid) {
          resolve(value)          
        } else {
          reject(new Error('not a valid email'));
        }
      });
    });
  });
  check('username', 'min character 3 and max character 14')
    .not()
    .isEmpty()
    .isLength({
      min:3,
      max:14
    });
  check('username', 'Only a-z, A-Z allowed')
    .matches(/[^a-zA-Z]/g);
    check('password', 'Password should be atleast 8 character')
    .not().
    isEmpty()
    .isLength({
      min:8,
      max: 25
    });
  check('password')
    .matches(/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])$/, "i")
    .withMessage('Password must include one lowercase, one uppercase, a number, and a special character');
  // to check if password match with password2
  check('password2', 'Password do not match, please check')
    .equals(req.body.password);
  // end of validation

    // check for errors during the validation
  var errors = validationResult(req);
  if(!errors.isEmpty()){
    return res.render('index').json({
      errors: errors.array(),
      // to return all input value back to the user if there was error during filling
      name: name,
      street_address: street_address,
      city: city,
      state: state,
      zip: zip,
      email: email,
      username: username,
    }); // end of error check, if no errors then create new user
  } 
  else {
    // console back the details
    var test = {
      name: name,
      street_address: street_address,
      city: city,
      state: state,
      email: email,
      username: username,
      password: password,
      ipAddress: ipAddress
    };

    console.log(test);
  }
});


  module.exports = router;