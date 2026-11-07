// One goroutine per waiting customer, the Go way.
// Usage: go run ./goroutines N
package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

func kb(file, key string) int {
	b, _ := os.ReadFile(file)
	for _, l := range strings.Split(string(b), "\n") {
		if strings.HasPrefix(l, key) {
			f := strings.Fields(strings.TrimPrefix(l, key))
			v, _ := strconv.Atoi(f[0])
			return v
		}
	}
	return -1
}

func main() {
	n, _ := strconv.Atoi(os.Args[1])
	open := make(chan struct{})
	var wg sync.WaitGroup
	kstack0 := kb("/proc/meminfo", "KernelStack:")
	t0 := time.Now()
	for range n {
		wg.Add(1)
		go func() { // wait, doing nothing
			defer wg.Done()
			<-open
		}()
	}
	took := time.Since(t0)
	fmt.Printf("goroutines started: %d\n", n)
	fmt.Printf("OS threads:         %d\n", kb("/proc/self/status", "Threads:"))
	fmt.Printf("time to start:      %.3f s\n", took.Seconds())
	fmt.Printf("memory used:        %d MB\n", kb("/proc/self/status", "VmRSS:")/1024)
	fmt.Printf("kernel stacks:      %d MB\n", (kb("/proc/meminfo", "KernelStack:")-kstack0)/1024)
	close(open)
	wg.Wait()
}
