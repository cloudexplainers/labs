package main

import "fmt"

type Team struct {
	Name string
	Wins int
}

func (t *Team) AddWin() {
	t.Wins++
	fmt.Println("in AddWin:", t.Name, "has", t.Wins)
}

func (t *Team) Record() string {
	return fmt.Sprintf("%s won %d", t.Name, t.Wins)
}

func main() {
	hawks := Team{Name: "Hawks"}
	hawks.AddWin()
	hawks.AddWin()
	fmt.Println("Season:", hawks.Record())
}
