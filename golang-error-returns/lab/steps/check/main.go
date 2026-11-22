package main

import (
	"fmt"
	"strconv"
	"strings"
)

func main() {
	orders := []string{"latte 450", "mocha 4.75", "tea 300"}
	total := 0
	for _, o := range orders {
		price := strings.Fields(o)[1]
		cents, err := strconv.Atoi(price)
		if err != nil {
			fmt.Println("skipped:", o, "-", err)
			continue
		}
		total += cents
	}
	fmt.Println("Sold:", len(orders), "drinks")
	fmt.Println("Total:", total, "cents")
}
