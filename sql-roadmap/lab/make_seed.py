#!/usr/bin/env python3
"""Writes lab/seed.sql: the book club's three tables and their rows (12 members, 30 books, 40 loans, 3 still out).
The members are made up; the books are real novels with their first publication year. Run: python3 lab/make_seed.py"""
from pathlib import Path

MEMBERS = ["Linda", "Rob", "Lena", "Omar", "Grace", "Paul", "Ruth", "Sam", "Nadia", "Priya", "Hugo", "Ellen"]
JOINED = ["2024-01-10", "2026-10-14", "2024-01-10", "2024-03-02", "2024-01-10", "2024-06-18", "2024-09-05",
          "2025-02-11", "2025-04-23", "2025-08-30", "2026-09-09", "2026-10-01"]
LOANS = {"Linda": 5, "Rob": 0, "Lena": 4, "Omar": 6, "Grace": 7, "Paul": 3, "Ruth": 5, "Sam": 2, "Nadia": 4,
         "Priya": 4, "Hugo": 0, "Ellen": 0}
BOOKS = [
    ("Pride and Prejudice", "Jane Austen", 1813), ("Frankenstein", "Mary Shelley", 1818),
    ("Moby-Dick", "Herman Melville", 1851), ("Middlemarch", "George Eliot", 1871),
    ("Dracula", "Bram Stoker", 1897), ("The Great Gatsby", "F. Scott Fitzgerald", 1925),
    ("Mrs Dalloway", "Virginia Woolf", 1925), ("Brave New World", "Aldous Huxley", 1932),
    ("Their Eyes Were Watching God", "Zora Neale Hurston", 1937), ("Rebecca", "Daphne du Maurier", 1938),
    ("The Grapes of Wrath", "John Steinbeck", 1939), ("Nineteen Eighty-Four", "George Orwell", 1949),
    ("The Catcher in the Rye", "J. D. Salinger", 1951), ("Fahrenheit 451", "Ray Bradbury", 1953),
    ("Things Fall Apart", "Chinua Achebe", 1958), ("To Kill a Mockingbird", "Harper Lee", 1960),
    ("Dune", "Frank Herbert", 1965), ("A Wizard of Earthsea", "Ursula K. Le Guin", 1968),
    ("The Left Hand of Darkness", "Ursula K. Le Guin", 1969), ("The Dispossessed", "Ursula K. Le Guin", 1974),
    ("Beloved", "Toni Morrison", 1987), ("The Remains of the Day", "Kazuo Ishiguro", 1989),
    ("The Secret History", "Donna Tartt", 1992), ("The God of Small Things", "Arundhati Roy", 1997),
    ("Life of Pi", "Yann Martel", 2001), ("Never Let Me Go", "Kazuo Ishiguro", 2005),
    ("The Road", "Cormac McCarthy", 2006), ("Wolf Hall", "Hilary Mantel", 2009),
    ("Station Eleven", "Emily St. John Mandel", 2014), ("Piranesi", "Susanna Clarke", 2020),
]
STILL_OUT = {"Grace", "Paul", "Nadia"}   # each has her or his latest loan still out


def q(s: str) -> str:
    return "'" + s.replace("'", "''") + "'"


sql = ["""CREATE TABLE members (
  id     integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name   text NOT NULL,
  joined date NOT NULL DEFAULT current_date
);
CREATE TABLE books (
  id     integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title  text NOT NULL,
  author text NOT NULL,
  year   integer NOT NULL
);
CREATE TABLE loans (
  id          integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  book_id     integer NOT NULL REFERENCES books (id),
  member_id   integer NOT NULL REFERENCES members (id),
  borrowed_on date NOT NULL,
  returned_on date
);"""]
sql.append("INSERT INTO members (name, joined) VALUES\n" +
           ",\n".join(f"  ({q(n)}, {q(d)})" for n, d in zip(MEMBERS, JOINED)) + ";")
sql.append("INSERT INTO books (title, author, year) VALUES\n" +
           ",\n".join(f"  ({q(t)}, {q(a)}, {y})" for t, a, y in BOOKS) + ";")
rows, book, day = [], 0, 0
order = [n for k in range(7) for n in MEMBERS if LOANS[n] > k]     # interleaved, like a real lending log
left = dict(LOANS)
for n in order:
    left[n] -= 1
    book = (book * 7 + 11) % len(BOOKS)
    day += 7
    month, dom = 1 + day // 28 if day // 28 < 11 else 11, 1 + day % 28
    borrowed = f"2026-{month:02d}-{dom:02d}"
    if n in STILL_OUT and left[n] == 0:
        returned = "NULL"
    else:
        rd = min(dom + 14, 28)
        returned = q(f"2026-{month:02d}-{rd:02d}")
    rows.append(f"  ({book + 1}, {MEMBERS.index(n) + 1}, {q(borrowed)}, {returned})")
assert len(rows) == 40
sql.append("INSERT INTO loans (book_id, member_id, borrowed_on, returned_on) VALUES\n" + ",\n".join(rows) + ";")
(Path(__file__).parent / "seed.sql").write_text("\n".join(sql) + "\n")
print("seed.sql:", len(MEMBERS), "members,", len(BOOKS), "books,", len(rows), "loans")
