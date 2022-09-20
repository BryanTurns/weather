const sqlite3 = require("sqlite3");
const { generateApiKey } = require("generate-api-key");
const db = new sqlite3.Database("test.db");
var express = require("express");
var router = express.Router();

router.post("/addUser/:key/:username", (req, res) => {
  let valid = false;
  // Get admin API key
  let newKey = generateApiKey();
  db.all("SELECT * FROM key WHERE user='admin'", [], (err, rows) => {
    if (err) {
      throw err;
    }
    // Check if req key = admin key
    if (rows[0].key == req.params.key) {
      valid = true;
    }
    // If key is invalid
    if (!valid) {
      return res.status(403).send("You do not have access to this page");
    }
    // If key is valid
    else {
      // Add new user to db
      db.run(
        "INSERT INTO key VALUES (?, ?)",
        [req.params.username, newKey],
        (err) => {
          if (err) {
            throw err;
          }
        }
      );
    }
    return res.status(200).send("Keys Updated: " + newKey);
  });
});

router.get("/getUsers", (req, res) => {
  db.all("SELECT * FROM key", [], (err, rows) => {
    if (err) {
      throw err;
    }
    users = [];
    rows.map((row) => {
      users.push(row.user);
    });
    res.json(users);
  });
});

module.exports = router;
