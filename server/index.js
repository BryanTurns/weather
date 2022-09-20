const express = require("express");
const PORT = process.env.PORT || 3001;
const app = express();
const weatherRouter = require("./routes/weather");
const adminRouter = require("./routes/admin");

app.use("/api/weather", weatherRouter);
app.use("/api/admin", adminRouter);
app.use(express.json());

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
