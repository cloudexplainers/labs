package main

import "fmt"

func main() {
	fmt.Println("open valve A")
	defer fmt.Println("close valve A")
	fmt.Println("open valve B")
	defer fmt.Println("close valve B")
	fmt.Println("open valve C")
	defer fmt.Println("close valve C")
	fmt.Println("watering done")
}
