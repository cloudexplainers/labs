package main

import (
	"fmt"
	"io"
	"net/http"
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
	for _, tea := range []string{"green", "black", "oolong"} {
		check(tea)
	}
	fmt.Println("all done in", time.Since(start).Round(time.Millisecond))
}
