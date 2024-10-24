const express = require('express')
const mysql = require('mysql')
const BodyParser = require("body-parser")
const app = express();

const http = require("http")
const server = http.createServer(app)
const {Server} = require("socket.io")
const io = new Server(server)

app.use(BodyParser.urlencoded({ ectended: true }))

app.set("view engine", "ejs")
app.set("views", "views")

const db = mysql.createConnection({
    host: "localhost",
    database: "miniChat",
    user: "root",
    password: "",
})

db.connect((err) => {
    if (err) throw err
    console.log("database connected...")
  
    app.get("/", (req, res) => {
    const sql = "SELECT * FROM chat"
        db.query(sql, (err, result) => {
            const users = JSON.parse(JSON.stringify(result))
            res.render("index", {users: users, title: "Tambah Anggota" })
        })
    })

    app.get("/chat", (req, res) => {
        res.render("chat", {title: "FORM LOGIN"})
    })

    app.post("/tambah", (req, res) => {
        const insertSql = `INSERT INTO chat (nama, password) VALUES ('${req.body.nama}', '${req.body.password}');`;
        db.query(insertSql, (err, result) => {
            if (err) throw err
            res.redirect("/");
        })
    })

})

app.listen(3000, () => {
    console.log("server ready...")
})