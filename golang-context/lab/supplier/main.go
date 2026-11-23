// The garden center's plant supplier, standing in for a slow outside service: every stock check takes 8 seconds.
// Built into the image and started with the container (port 9000); it is not part of John's code.
package main

import (
	"fmt"
	"log"
	"net/http"
	"strings"
	"time"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(8 * time.Second)
		fmt.Fprintf(w, "%s: 12 in stock", strings.TrimPrefix(r.URL.Path, "/"))
	})
	log.Fatal(http.ListenAndServe("localhost:9000", nil))
}
