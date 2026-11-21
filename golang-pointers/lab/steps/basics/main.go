package main

import "fmt"

func main() {
	walks := 5
	p := &walks
	fmt.Println(p)
	*p = 6
	fmt.Println(walks)
	var q *int
	fmt.Println(q)
}
