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
		f, err := os.Open(name)
		if err != nil {
			fmt.Printf("file %d of %d: %v\n", i+1, len(files), err)
			os.Exit(1)
		}
		defer f.Close()
		total += sum(f)
	}
	fmt.Println("files read:", len(files), "litres:", total)
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
