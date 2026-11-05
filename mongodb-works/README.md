# How a NoSQL Database Like MongoDB Works

Video: https://youtu.be/4HCtsg-IwvA  
Written version: https://cloudexplainers.com/how-a-nosql-database-like-mongodb-works/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/catalog.js`](lab/catalog.js)

## Commands, in the order the video runs them

### MongoDB

```sh
rs0 [primary] bookshop> show collections
rs0 [primary] bookshop> db.books.insertOne({title: "Dune", author: {name: "Frank Herbert", born: 1920}, year: 1965, tags: ["sci-fi", "classic"], price: 9.99, stock: 3})
rs0 [primary] bookshop> show collections
```

### Documents

```sh
rs0 [primary] bookshop> db.books.findOne({title: "Dune"})
```

### Collections

```sh
rs0 [primary] bookshop> db.books.insertOne({title: "The Hobbit", author: {name: "J.R.R. Tolkien"}, year: 1937, stock: 5, signed: true})
rs0 [primary] bookshop> db.books.find({}, {_id: 0, title: 1, year: 1, stock: 1, signed: 1})
```

### The ID

```sh
rs0 [primary] bookshop> db.books.findOne({title: "Dune"})._id
rs0 [primary] bookshop> db.books.findOne({title: "Dune"})._id.getTimestamp()
```

### Queries

```sh
rs0 [primary] bookshop> db.books.find({"author.name": "Frank Herbert"}, {_id: 0, title: 1})
rs0 [primary] bookshop> db.books.find({tags: "sci-fi"}, {_id: 0, title: 1})
rs0 [primary] bookshop> db.books.find({year: {$lt: 1950}}, {_id: 0, title: 1, year: 1})
rs0 [primary] bookshop> db.books.updateOne({title: "Dune"}, {$inc: {stock: -1}})
rs0 [primary] bookshop> db.books.findOne({title: "Dune"}, {_id: 0, title: 1, stock: 1})
```

### Indexes

```sh
rs0 [primary] bookshop> db.catalog.countDocuments()
rs0 [primary] bookshop> db.catalog.find({isbn: "978-1000864192"}).explain("executionStats").executionStats
rs0 [primary] bookshop> db.catalog.createIndex({isbn: 1})
rs0 [primary] bookshop> db.catalog.find({isbn: "978-1000864192"}).explain("executionStats").executionStats
```

### On disk

```sh
rs0 [primary] bookshop> db.serverStatus().storageEngine.name
rs0 [primary] bookshop> db.catalog.dataSize()
rs0 [primary] bookshop> db.catalog.storageSize()
```

### Replica sets

```sh
rs0 [primary] bookshop> rs.status().members.map(m => m.name + "  " + m.stateStr)
rs0 [primary] bookshop> db.books.insertOne({title: "Neuromancer", author: {name: "William Gibson"}, year: 1984, stock: 2}, {writeConcern: {w: "majority"}})
rs0 [direct: secondary] bookshop> db.getSiblingDB("local").oplog.rs.find({ns: "bookshop.books"}).sort({$natural: -1}).limit(1)
```

### A server crashes

```sh
docker kill mongo1
rs0 [primary] bookshop> rs.status().members.map(m => m.name + "  " + m.stateStr)
rs0 [primary] bookshop> db.books.findOne({title: "Neuromancer"}, {_id: 0, title: 1, year: 1})
rs0 [primary] bookshop> db.books.updateOne({title: "Neuromancer"}, {$inc: {stock: -1}})
docker start mongo1
rs0 [primary] bookshop> rs.status().members.map(m => m.name + "  " + m.stateStr)
rs0 [direct: secondary] bookshop> db.books.findOne({title: "Neuromancer"}, {_id: 0, title: 1, stock: 1})
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
