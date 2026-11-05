// The tea suppliers' stock service: every answer takes about one second.
package main

import (
	"fmt"
	"net/http"
	"time"
)

var stock = map[string]int{"green": 12, "black": 30, "oolong": 7}

func main() {
	http.HandleFunc("/stock", func(w http.ResponseWriter, r *http.Request) {
		tea := r.URL.Query().Get("tea")
		if r.URL.Query().Get("slow") != "" {
			time.Sleep(5 * time.Second)
		} else {
			time.Sleep(1 * time.Second)
		}
		fmt.Fprintf(w, "%d", stock[tea])
	})
	http.ListenAndServe("127.0.0.1:8080", nil)
}
