package main

import (
	"fmt"
	"os"
	"runtime"
	"strings"
	"sync"
	"time"
)

func threads() string {
	b, _ := os.ReadFile("/proc/self/status")
	for _, l := range strings.Split(string(b), "\n") {
		if strings.HasPrefix(l, "Threads:") {
			return strings.TrimSpace(strings.TrimPrefix(l, "Threads:"))
		}
	}
	return "?"
}

func main() {
	var wg sync.WaitGroup
	for range 100000 {
		wg.Add(1)
		go func() {
			defer wg.Done()
			time.Sleep(3 * time.Second)
		}()
	}
	time.Sleep(time.Second)
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	fmt.Println("goroutines running:", runtime.NumGoroutine())
	fmt.Println("OS threads:        ", threads())
	fmt.Println("CPU cores:         ", runtime.NumCPU())
	fmt.Printf("stack memory:       %d MB\n", m.StackInuse>>20)
	wg.Wait()
}
