package main

import (
	"fmt"
	"io"
	"net/http"
	"strconv"
	"time"
)

func check(url string, results chan<- int) {
	resp, err := http.Get(url)
	if err != nil {
		return
	}
	n, _ := io.ReadAll(resp.Body)
	resp.Body.Close()
	count, _ := strconv.Atoi(string(n))
	results <- count
}

func main() {
	start := time.Now()
	results := make(chan int, 1)
	go check("http://127.0.0.1:8080/stock?tea=oolong&slow=1", results)
	select {
	case n := <-results:
		fmt.Println("oolong in stock:", n)
	case <-time.After(2 * time.Second):
		fmt.Println("oolong: no answer, gave up")
	}
	fmt.Println("all done in", time.Since(start).Round(time.Millisecond))
}
