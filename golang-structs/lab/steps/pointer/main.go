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
	}
	top := &board[0]
	top.Points = 99950
	fmt.Println(top.Points)
	fmt.Println(board[0].Points)
}
