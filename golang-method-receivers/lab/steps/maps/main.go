package main

import "fmt"

type Team struct {
	Name string
	Wins int
}

func (t *Team) AddWin() {
	t.Wins++
}

func main() {
	league := map[string]Team{
		"Hawks": {Name: "Hawks"},
		"Owls":  {Name: "Owls"},
	}
	league["Hawks"].AddWin()
	fmt.Println("Hawks wins:", league["Hawks"].Wins)
}
