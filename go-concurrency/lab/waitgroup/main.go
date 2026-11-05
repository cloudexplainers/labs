package main

import (
	"fmt"
	"io"
	"net/http"
	"sync"
	"time"
)

func check(tea string) {
	resp, _ := http.Get("http://127.0.0.1:8080/stock?tea=" + tea)
	n, _ := io.ReadAll(resp.Body)
	resp.Body.Close()
	fmt.Println(tea, "in stock:", string(n))
}

func main() {
	start := time.Now()
	var wg sync.WaitGroup
	for _, tea := range []string{"green", "black", "oolong"} {
		wg.Add(1)
		go func() {
			defer wg.Done()
			check(tea)
		}()
	}
	wg.Wait()
	fmt.Println("all done in", time.Since(start).Round(time.Millisecond))
}
