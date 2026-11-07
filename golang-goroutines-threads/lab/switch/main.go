// Two goroutines hand a token back and forth over channels.
package main

import (
	"fmt"
	"time"
)

const rounds = 200000

func main() {
	ping, pong := make(chan int), make(chan int)
	go func() {
		for v := range ping {
			pong <- v
		}
	}()
	t0 := time.Now()
	for i := range rounds {
		ping <- i
		<-pong
	}
	ns := float64(time.Since(t0).Nanoseconds()) / (2 * rounds)
	fmt.Printf("goroutines, one hand-off: %.0f ns\n", ns)
}
