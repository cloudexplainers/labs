package main

import "fmt"

func main() {
	fmt.Println(len(grow(10000)), len(presized(10000)))
}

// grow appends to a slice that starts with no room.
func grow(n int) []int {
	var s []int
	for i := range n {
		s = append(s, i)
	}
	return s
}

// presized asks make for all the room up front.
func presized(n int) []int {
	s := make([]int, 0, n)
	for i := range n {
		s = append(s, i)
	}
	return s
}
