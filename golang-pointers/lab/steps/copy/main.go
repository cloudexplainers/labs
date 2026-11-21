package main

import "fmt"

type Dog struct {
	Name  string
	Walks int
}

func addWalk(d Dog) {
	d.Walks++
}

func main() {
	rex := Dog{Name: "Rex"}
	addWalk(rex)
	addWalk(rex)
	fmt.Println(rex.Name, "walks:", rex.Walks)
}
