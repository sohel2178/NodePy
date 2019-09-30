const Express = require("express");
const morgan = require("morgan");
const bodyParser = require("body-parser");

const app = Express();

app.get("/name", callName);

let bars = [
  {
    title: "BarA",
    length: 8.5,
    number_of_bars: 2000
  },
  {
    title: "BarB",
    length: 7.5,
    number_of_bars: 2000
  },
  {
    title: "BarA",
    length: 3.5,
    number_of_bars: 2000
  }
];

var ttt = {
  fName: "Sohel",
  lName: "Ahmed"
};
var jjj = JSON.stringify(bars);

function callName(req, res) {
  var spawn = require("child_process").spawn;
  var process = spawn("python", ["./test.py", jjj, "Ahmed"]);

  process.stdout.on("data", function(data) {
    console.log(data.toString());
    res.send(data.toString());
  });
}

// pyshell.on("message", function(message) {
//   // received a message sent from the Python script (a simple "print" statement)
//   console.log(message);
// });

app.use(morgan("dev"));

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }));
// parse application/json
app.use(bodyParser.json());

// For Support Cross Origin Request
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*"); // '*' for any
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept, Authorization"
  );

  if (req.method === "OPTIONS") {
    res.header("Access-Control-Allow-Methods", "GET,POST,PUT,PATCH,DELETE");
    return res.status(200).json({});
  }

  next();
});

// All Of Our Routes Goes Here

// Handling Error If No Request is Match to Our Route
app.use((req, res, next) => {
  const error = new Error();
  error.status = 400;
  error.message = "Route not Match";
  // Send Error to the Next
  next(error);
});

// This is Handle All Error including Route and Database Error
app.use((error, req, res, next) => {
  res.status(error.status || 500);
  res.json({
    error: {
      message: error.message
    }
  });
});

module.exports = app;
