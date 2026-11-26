package main

import "fmt"

func main() {
	var crates []int // nil: no array behind it yet
	fmt.Println("nil?", crates == nil, "len", len(crates), "cap", cap(crates))

	for bin := 1; bin <= 20; bin++ {
		before := cap(crates)
		crates = append(crates, bin)
		if cap(crates) != before {
			fmt.Println("len", len(crates), "cap", cap(crates), "<- new, bigger array")
		}
	}
}
