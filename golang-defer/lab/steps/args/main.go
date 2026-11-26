package main

import "fmt"

func main() {
	litres := 0
	defer fmt.Println("litres used:", litres)
	litres += 12 // bed 1
	litres += 30 // bed 2
	fmt.Println("watering done")
}
