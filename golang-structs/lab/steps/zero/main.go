package main

import "fmt"

type Score struct {
	Player string
	Points int
	Game   string
	Date   string
}

func main() {
	var s Score
	fmt.Println(s)
	fmt.Printf("%+v\n", s)
}
