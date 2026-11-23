package main

import "fmt"

type Team struct {
	Name string
	Wins int
}

func (t *Team) AddWin() {
	t.Wins++
}

func (t *Team) Record() string {
	return fmt.Sprintf("%s won %d", t.Name, t.Wins)
}

type Scorer interface {
	AddWin()
}

func main() {
	hawks := Team{Name: "Hawks"}
	var s Scorer = &hawks
	s.AddWin()
	fmt.Println("Season:", hawks.Record())
}
