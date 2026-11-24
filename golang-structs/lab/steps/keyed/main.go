package main

import "fmt"

type Score struct {
	Player string
	Points int
	Game   string
	Date   string
}

func main() {
	board := []Score{
		{Player: "SUE", Points: 98200, Game: "Galaxy Run"},
		{Player: "RICH", Points: 87150, Game: "Galaxy Run", Date: "Nov 22"},
		{Player: "MAY", Points: 64300, Game: "Pinball Pete"},
	}
	for _, s := range board {
		fmt.Printf("%+v\n", s)
	}
}
