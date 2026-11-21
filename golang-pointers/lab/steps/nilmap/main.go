package main

import "fmt"

type Dog struct {
	Name  string
	Walks int
}

func (d *Dog) Walk() {
	d.Walks++
}

func main() {
	dogs := map[string]*Dog{"Rex": {Name: "Rex"}, "Bella": {Name: "Bella"}}
	dogs["Rex"].Walk()
	dogs["Max"].Walk()
	fmt.Println("walks booked")
}
