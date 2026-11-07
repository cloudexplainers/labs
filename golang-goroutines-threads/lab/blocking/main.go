// 100 goroutines wait two ways: on the Go runtime, or stuck in a blocking system call.
package main

import (
	"fmt"
	"os"
	"strings"
	"syscall"
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
	for range 100 {
		go time.Sleep(time.Hour) // Go parks it: no thread needed
	}
	time.Sleep(time.Second)
	fmt.Println("100 sleeping goroutines, OS threads:", threads())

	var p [2]int
	syscall.Pipe(p[:]) // a plain blocking pipe that nobody writes to
	for range 100 {
		go func() {
			buf := make([]byte, 1)
			syscall.Read(p[0], buf) // the kernel holds the whole thread here
		}()
	}
	time.Sleep(time.Second)
	fmt.Println("100 more stuck in a system call, OS threads:", threads())
}
