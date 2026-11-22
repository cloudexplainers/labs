package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/fs"
	"os"
)

type Schedule struct {
	Flights []string `json:"flights"`
}

func loadSchedule(path string) (*Schedule, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read schedule: %v", err)
	}
	var s Schedule
	if err := json.Unmarshal(data, &s); err != nil {
		return nil, fmt.Errorf("parse %s: %v", path, err)
	}
	return &s, nil
}

func main() {
	s, err := loadSchedule("schedule.json")
	if errors.Is(err, fs.ErrNotExist) {
		fmt.Println("no schedule yet, starting an empty one")
		s, err = &Schedule{}, nil
	}
	if err != nil {
		fmt.Println("could not load:", err)
		return
	}
	fmt.Println("Flights today:", len(s.Flights))
}
