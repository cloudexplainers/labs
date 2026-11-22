package main

import (
	"fmt"

	"github.com/fatih/color"
)

func main() {
	fmt.Println("RIVERSIDE STATION - DEPARTURES")
	fmt.Println("08:14  Harbor Line   platform 2  ", color.GreenString("on time"))
	fmt.Println("08:22  Valley Line   platform 1  ", color.YellowString("delayed 4 min"))
}
