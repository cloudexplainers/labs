package main

import (
	"encoding/json"
	"fmt"
)

type Score struct {
	Player string `json:"player"`
	Points int    `json:"points"`
	Game   string `json:"game"`
	Date   string `json:"date"`
}

func main() {
	s := Score{Player: "RICH", Points: 87150, Game: "Galaxy Run", Date: "Nov 22"}
	out, _ := json.Marshal(s)
	fmt.Println(string(out))
}
