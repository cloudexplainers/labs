package main

import "fmt"

type Catch struct {
	Fish  string
	Grams int
}

func main() {
	catches := []Catch{
		{"mackerel", 1500},
		{"sea bass", 2400},
		{"cod", 4100},
		{"mackerel", 1100},
		{"pollock", 3200},
	}

	for i, c := range catches {
		fmt.Println(i, c.Fish, c.Grams)
	}
}
