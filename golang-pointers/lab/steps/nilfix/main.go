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
	d, ok := dogs["Max"]
	if !ok {
		fmt.Println("no dog called Max")
		return
	}
	d.Walk()
}
