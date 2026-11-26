// The card service Tom's card reader talks to (a stand-in for a real payment
// company's API). Each charge takes about a second, like a real network round trip.
package main

import (
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"
)

func main() {
	http.HandleFunc("/charge", func(w http.ResponseWriter, r *http.Request) {
		cents, err := strconv.Atoi(r.URL.Query().Get("cents"))
		if err != nil || cents <= 0 {
			http.Error(w, "bad amount", http.StatusBadRequest)
			return
		}
		time.Sleep(time.Second)
		log.Printf("charged $%d.%02d to a real card", cents/100, cents%100)
		fmt.Fprintln(w, "approved")
	})
	log.Fatal(http.ListenAndServe("127.0.0.1:9000", nil))
}
