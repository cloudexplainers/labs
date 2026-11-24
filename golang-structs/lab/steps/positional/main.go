package main

import "fmt"

type Score struct {
	Player string
	Points int
	Game   string
}

func main() {
	board := []Score{
		{"SUE", 98200, "Galaxy Run"},
		{"RICH", 87150, "Galaxy Run"},
		{"MAY", 64300, "Pinball Pete"},
	}
	for _, s := range board {
		fmt.Println(s)
	}
}
