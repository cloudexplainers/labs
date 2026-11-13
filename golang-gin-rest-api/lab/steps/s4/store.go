package main

type Plant struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Light string `json:"light"`
	Stock int    `json:"stock"`
}

var plants = map[int]Plant{
	1: {1, "Fern", "shade", 12},
	2: {2, "Basil", "sun", 40},
	3: {3, "Olive tree", "sun", 2},
}

var nextID = 3
