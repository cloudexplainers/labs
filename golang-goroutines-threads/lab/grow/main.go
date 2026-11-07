// How deep can one goroutine go? Each call adds a frame to its stack.
package main

import "fmt"

func depth(n int) int {
	var pad [64]byte // a little room per call, like a real function
	if n == 0 {
		return int(pad[0])
	}
	return depth(n-1) + int(pad[n%64]) + 1
}

func main() {
	done := make(chan int)
	go func() { done <- depth(1000000) }()
	fmt.Println("calls deep:", <-done)
}
