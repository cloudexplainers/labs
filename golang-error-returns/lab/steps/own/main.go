package main

import (
	"errors"
	"fmt"
	"strconv"
	"strings"
)

func priceCents(order string) (int, error) {
	fields := strings.Fields(order)
	if len(fields) != 2 {
		return 0, errors.New("no price on the order")
	}
	cents, err := strconv.Atoi(fields[1])
	if err != nil {
		return 0, fmt.Errorf("%q: price must be whole cents", order)
	}
	return cents, nil
}

func main() {
	orders := []string{"latte 450", "mocha 4.75", "espresso", "tea 300"}
	total := 0
	for _, o := range orders {
		cents, err := priceCents(o)
		if err != nil {
			fmt.Println("problem:", err)
			continue
		}
		total += cents
	}
	fmt.Println("Total:", total, "cents")
}
