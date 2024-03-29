const express = require("express");
const { spawn } = require("child_process");
const multer = require("multer");
const path = require("path");
const bodyParser = require("body-parser");

const app = express();

app.use(bodyParser.urlencoded({ extended: false }));

const PORT = 8000;

const options = {
  root: path.join(__dirname),
};

const fileStorage = multer.diskStorage({
  destination: (req, file, cb) => {
    if (req.files?.input) {
      cb(null, path.join(__dirname, "Input"));
    } else if (req.files?.images) {
      cb(null, path.join(__dirname, "BubbleSheet/dataset/Input"));
    }
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

app.use((_req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader(
    "Access-Control-Allow-Methods",
    "GET,POST,PUT,DELETE,PATCH,OPTIONS"
  );
  res.setHeader("Access-Control-Allow-Headers", "Content-Type,Authorization");
  next();
});

app.use(
  multer({ storage: fileStorage, fileFilter: fileFilter }).fields([
    { name: "input", maxCount: 1 },
    { name: "images", maxCount: 100 },
  ])
);

app.post("/", (req, res) => {
  const codesChoice = req.body.codesChoice;
  const digitsChoice = req.body.digitsChoice;

  const python = spawn("python", [
    "excel.py",
    codesChoice.toString(),
    digitsChoice.toString(),
  ]);

  python.on("close", (code) => {
    res.setHeader("Content-Type", "application/vnd.ms-excel");
    res.sendFile("autoFiller.xls", options, function (err) {
      if (err) {
        console.log(err.message);
      } else {
        console.log("Sent");
      }
    });
  });
});

app.post("/bubble", (req, res) => {
  const python = spawn("python", ["BubbleSheet/bubbleScript.py"]);

  python.on("close", (code) => {
    res.setHeader(
      "Content-Type",
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    );
    res.sendFile(
      path.join("BubbleSheet", "answers.xlsx"),
      options,
      function (err) {
        if (err) {
          console.log(err.message);
        } else {
          console.log("Sent");
        }
      }
    );
  });
});

app.listen(PORT, () => {
  console.log(`Started on port ${PORT}`);
});
