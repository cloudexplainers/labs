package main

import "fmt"

func main() {
	picked := []int{14, 9, 11} // bins picked in rows 1, 2 and 3

	perRow := make([]int, 0, 3)
	for _, n := range picked {
		perRow = append(perRow, n)
	}
	fmt.Println(perRow, "len", len(perRow), "cap", cap(perRow))
}
