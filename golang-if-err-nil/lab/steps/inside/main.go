package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type Schedule struct {
	Flights []string `json:"flights"`
}

func loadSchedule(path string) (*Schedule, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var s Schedule
	if err := json.Unmarshal(data, &s); err != nil {
		return nil, err
	}
	return &s, nil
}

func main() {
	s, err := loadSchedule("schedule.json")
	if err != nil {
		fmt.Println("could not load:", err)
		return
	}
	fmt.Println("Flights today:", len(s.Flights))
}
