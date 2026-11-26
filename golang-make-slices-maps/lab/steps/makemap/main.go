package main

import "fmt"

func main() {
	bins := make(map[string]int)

	fmt.Println("Gala bins so far:", bins["Gala"])
	bins["Gala"] += 14
	bins["Fuji"] += 9
	bins["Gala"] += 11
	fmt.Println("bins:", bins, "varieties:", len(bins))
}
