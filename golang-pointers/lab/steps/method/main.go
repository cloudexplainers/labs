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
	rex := Dog{Name: "Rex"}
	rex.Walk()
	rex.Walk()
	fmt.Println(rex.Name, "walks:", rex.Walks)
}
