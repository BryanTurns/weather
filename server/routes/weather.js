const sqlite3 = require("sqlite3");
const db = new sqlite3.Database("test.db");
var express = require("express");
var router = express.Router();

// Get weather
router.get("/:key", (req, res) => {
  console.log("WEATHER API HIT");
  db.all("SELECT key FROM key", [], (err, rows) => {
    let found = false;
    let user = "";
    // if there is an error with the request
    if (err) {
      throw err;
    }

    // for each key in db check if it matches the request key
    rows.map((row) => {
      if (row.key == req.params.key) {
        found = true;
        user = row[0];
      }
    });
    // If not valid key
    if (!found) {
      return res.status(403).send("You do not have access to this page");
    } else {
      db.all("SELECT temperature, timsestamp FROM weather", [], (err, rows) => {
        if (err) throw err;
        return res.json(rows);
      });
    }
  });
});

// Post data to server db
router.post("/:key", (req, res) => {
  // Get key data from db
  db.all("SELECT key FROM key", [], (err, rows) => {
    let found = false;
    let user = "";
    // if there is an error with the request
    if (err) {
      throw err;
    }

    // for each key in db check if it matches the request key
    rows.map((row) => {
      if (row.key == req.params.key) {
        found = true;
        user = row[0].user;
      }
    });
    // If not valid key
    if (!found) {
      res.status(403).send("You do not have access to this page");
      return;
    }
    // If valid API key
    else {
      db.run("INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?)", [
        req.body.data.pressure,
        req.body.data.temperature,
        req.body.data.hum,
        req.body.data.gas,
        req.body.data.timestamp,
        req.body.data.uv,
        req.body.data.lux,
      ]);
      res.status(200).send("DATA POST SUCCESS");
      console.log(user + ":");
      console.log(req.body.data);
      console.log("\n");
    }
  });
});

module.exports = router;
