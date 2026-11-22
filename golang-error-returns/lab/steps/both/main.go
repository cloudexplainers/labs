package main

import (
	"fmt"
	"os"
	"strconv"
)

func main() {
	n, err := strconv.Atoi("450")
	fmt.Println(n, err)
	n, err = strconv.Atoi("4.75")
	fmt.Println(n, err)
	f, err := os.Open("menu.txt")
	fmt.Println(f, err)
}
