package main

import "fmt"

func water(bed string, readings []int) {
	fmt.Println("valve open:", bed)
	defer fmt.Println("valve closed:", bed)
	fmt.Println("moisture:", readings[2])
}

func main() {
	water("bed 3", []int{41, 38})
}
