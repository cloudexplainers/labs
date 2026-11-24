package main

import "fmt"

func main() {
	for trip := range 3 {
		fmt.Println("trip", trip+1, "of 3")
	}
}
