// Ana's kettle shop in MongoDB (P009): the same data as schema.sql. Loaded off-screen by demo.sh.
db = db.getSiblingDB("shop");
db.customers.insertMany([
  { _id: 1, name: "Ben", email: "ben@example.com" },
  { _id: 2, name: "Cara", email: "cara@example.com" },
  { _id: 3, name: "Dev", email: "dev@example.com" },
]);
db.products.insertMany([
  { _id: 1, name: "Copper kettle", price: 89.0, stock: 1 },
  { _id: 2, name: "Glass kettle", price: 54.0, stock: 12 },
  { _id: 3, name: "Travel kettle", price: 32.5, stock: 30 },
]);
const day = new Date(new Date().toISOString().slice(0, 10));
db.orders.insertMany([
  { _id: 1001, customer_id: 1, placed: day, items: [
      { product_id: 2, name: "Glass kettle", qty: 1, price: 54.0 },
      { product_id: 3, name: "Travel kettle", qty: 2, price: 32.5 } ] },
  { _id: 1002, customer_id: 2, placed: day, items: [
      { product_id: 3, name: "Travel kettle", qty: 1, price: 32.5 } ] },
  { _id: 1003, customer_id: 1, placed: day, items: [
      { product_id: 2, name: "Glass kettle", qty: 1, price: 54.0 } ] },
]);
db.products.createIndex({ name: 1 }, { unique: true });
print("seeded");
