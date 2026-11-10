# Every SQL Join Type in 10 Minutes

Video: https://youtu.be/4d7N3o7VitM  
Written version: https://cloudexplainers.com/every-sql-join-type-in-10-minutes/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/schema.sql`](lab/schema.sql)

## Commands, in the order the video runs them

### Where did Ben go?

```sh
shop=# SELECT name, tea FROM customers c JOIN orders o ON o.customer_id = c.id;
```

### Inner join

```sh
shop=# SELECT * FROM customers;
shop=# SELECT * FROM orders;
```

### Left join

```sh
shop=# SELECT name, tea FROM customers c LEFT JOIN orders o ON o.customer_id = c.id;
shop=# SELECT name, tea FROM customers c LEFT JOIN orders o ON o.customer_id = c.id WHERE tea = 'Sencha';
shop=# SELECT name, tea FROM customers c LEFT JOIN orders o ON o.customer_id = c.id AND tea = 'Sencha';
```

### Right join

```sh
shop=# SELECT name, tea FROM customers c RIGHT JOIN orders o ON o.customer_id = c.id;
shop=# SELECT name, tea FROM orders o LEFT JOIN customers c ON o.customer_id = c.id;
```

### Full outer join

```sh
shop=# SELECT name, tea FROM customers c FULL JOIN orders o ON o.customer_id = c.id;
```

### Cross join

```sh
shop=# SELECT tea, size FROM teas CROSS JOIN sizes;
shop=# SELECT count(*) FROM customers, orders;
```

### Self join

```sh
shop=# SELECT c.name, r.name AS referred_by FROM customers c JOIN customers r ON r.id = c.referred_by;
```

### Anti and semi join

```sh
shop=# SELECT name FROM customers c LEFT JOIN orders o ON o.customer_id = c.id WHERE o.id IS NULL;
shop=# SELECT name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
shop=# SELECT name FROM customers WHERE id NOT IN (SELECT customer_id FROM orders);
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
