package main

import "fmt"

type Dog struct {
	Name  string
	Walks int
}

func NewDog(name string) *Dog {
	d := Dog{Name: name}
	return &d
}

func main() {
	max := NewDog("Max")
	max.Walks++
	fmt.Println(max.Name, "walks:", max.Walks)
}
