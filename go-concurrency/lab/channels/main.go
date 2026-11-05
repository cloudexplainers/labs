package main

import (
	"fmt"
	"io"
	"net/http"
	"strconv"
	"time"
)

func check(tea string, results chan<- int) {
	resp, _ := http.Get("http://127.0.0.1:8080/stock?tea=" + tea)
	n, _ := io.ReadAll(resp.Body)
	resp.Body.Close()
	count, _ := strconv.Atoi(string(n))
	results <- count
}

func main() {
	start := time.Now()
	teas := []string{"green", "black", "oolong"}
	results := make(chan int)
	for _, tea := range teas {
		go check(tea, results)
	}
	total := 0
	for range teas {
		total += <-results
	}
	fmt.Println("total in stock:", total)
	fmt.Println("all done in", time.Since(start).Round(time.Millisecond))
}
