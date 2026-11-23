package main

import "fmt"

type Team struct {
	Name string
	Wins int
}

func (t Team) AddWin() {
	t.Wins++
	fmt.Println("in AddWin:", t.Name, "has", t.Wins)
}

func main() {
	hawks := Team{Name: "Hawks"}
	hawks.AddWin()
	hawks.AddWin()
	fmt.Println("Season:", hawks.Name, "wins", hawks.Wins)
}
