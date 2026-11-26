package main

import "fmt"

func water(bed string, wet bool) {
	fmt.Println("valve open:", bed)
	defer fmt.Println("valve closed:", bed)
	if wet {
		fmt.Println(bed, "is already wet, stop early")
		return
	}
	fmt.Println("watering", bed)
}

func main() {
	water("bed 1", false)
	water("bed 2", true)
}
