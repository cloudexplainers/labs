package main

import "fmt"

type Dog struct {
	Name  string
	Walks int
}

func addWalk(d *Dog) {
	d.Walks++
	fmt.Printf("addWalk's d: %p  walks %d\n", d, d.Walks)
}

func main() {
	rex := Dog{Name: "Rex"}
	fmt.Printf("main's rex:   %p\n", &rex)
	addWalk(&rex)
	addWalk(&rex)
	fmt.Println(rex.Name, "walks:", rex.Walks)
}
