package main

import "fmt"

func main() {
	results := make(chan int)
	results <- 12
	fmt.Println(<-results)
}
