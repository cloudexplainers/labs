package main

import (
	"fmt"
	"maps"
	"slices"
)

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
	for i := range catches {
		catches[i].Grams -= 300
	}

	totals := map[string]int{}
	for _, c := range catches {
		totals[c.Fish] += c.Grams
	}

	for _, fish := range slices.Sorted(maps.Keys(totals)) {
		fmt.Print(fish, " ", totals[fish], "   ")
	}
	fmt.Println()
}
