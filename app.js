const express = require("express");
const { spawn } = require("child_process");
const multer = require("multer");
const path = require("path");
const bodyParser = require("body-parser");

app.use(bodyParser.urlencoded({ extended: false }));

const port = 3000;

const app = express();

const fileStorage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, path.join(__dirname, "Input"));
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  },
});

const fileFilter = (req, file, cb) => {
  if (
    file.mimetype === "image/png" ||
    file.mimetype === "image/jpg" ||
    file.mimetype === "image/jpeg"
  ) {
    cb(null, true);
  } else {
    cb(null, false);
  }
};

app.use(
  multer({ storage: fileStorage, fileFilter: fileFilter }).single("input")
);

app.get("/", (req, res) => {
  let dataToSend;

  const codesChoice = req.body.codesChoice;
  const digitsChoice = req.body.digitsChoice;

  const python = spawn("python", ["excel.py", codesChoice, digitsChoice]);

  python.stdout.on("data", function (data) {
    dataToSend = data.toString();
  });

  python.on("close", (code) => {
    res.send(dataToSend);
  });
});

app.listen(port, () => {
  console.log(`Started on port ${port}`);
});
