// The bookshop's catalogue for P074's index demo: 200,000 made-up entries, loaded off-screen by demo_driver.py.
// Each has a unique ISBN-like code, so a lookup by isbn matches exactly one document.
db = db.getSiblingDB("bookshop");
const batch = [];
for (let i = 0; i < 200000; i++) {
  batch.push({
    isbn: "978-" + String(1000000000 + i * 7).slice(0, 10),
    title: "Catalogue book " + i,
    price: 5 + (i % 40),
    stock: i % 12,
  });
  if (batch.length === 10000) { db.catalog.insertMany(batch); batch.length = 0; }
}
print(db.catalog.countDocuments());
