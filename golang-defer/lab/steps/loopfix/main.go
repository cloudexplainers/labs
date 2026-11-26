package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
)

func main() {
	files, _ := filepath.Glob("readings/*.log")
	total := 0
	for i, name := range files {
		n, err := readLog(name)
		if err != nil {
			fmt.Printf("file %d of %d: %v\n", i+1, len(files), err)
			os.Exit(1)
		}
		total += n
	}
	fmt.Println("files read:", len(files), "litres:", total)
}

// readLog opens one log, adds it up, and closes it when it returns.
func readLog(name string) (int, error) {
	f, err := os.Open(name)
	if err != nil {
		return 0, err
	}
	defer f.Close()
	return sum(f), nil
}

// sum adds up the litres in one watering log, one number per line.
func sum(f *os.File) int {
	total := 0
	sc := bufio.NewScanner(f)
	for sc.Scan() {
		n, _ := strconv.Atoi(sc.Text())
		total += n
	}
	return total
}
