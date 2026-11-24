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

	// take off the 300 g bucket
	for i := range catches {
		catches[i].Grams -= 300
	}

	fmt.Println("-- log --")
	for _, c := range catches {
		fmt.Println(c.Fish, c.Grams)
	}
}
