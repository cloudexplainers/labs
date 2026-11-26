package main

import "fmt"

func main() {
	var bins map[string]int

	fmt.Println("Gala bins so far:", bins["Gala"])
	bins["Gala"] += 14
	fmt.Println("Gala bins:", bins["Gala"])
}
