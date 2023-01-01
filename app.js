const express = require("express");
const { spawn } = require("child_process");
const multer = require("multer");
const path = require("path");
const bodyParser = require("body-parser");

const app = express();

app.use(bodyParser.urlencoded({ extended: false }));

const port = 8000;

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
    res.status(200).json({
      message: "Success",
    });
  });
});

app.post("/bubble", (req, res) => {
  const python = spawn("python", ["BubbleSheet/bubbleScript.py"]);

  python.on("close", (code) => {
    res.status(200).json({
      message: "Success",
    });
  });
});

app.listen(port, () => {
  console.log(`Started on port ${port}`);
});
