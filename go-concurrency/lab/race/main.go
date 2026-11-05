package main

import (
	"fmt"
	"sync"
)

func main() {
	orders := 0
	var wg sync.WaitGroup
	for range 1000 {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for range 1000 {
				orders++
			}
		}()
	}
	wg.Wait()
	fmt.Println("orders counted:", orders, "of 1000000")
}
