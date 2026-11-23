package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net/http"
	"time"
)

func askSupplier(ctx context.Context, plant string) (string, error) {
	url := "http://localhost:9000/" + plant
	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		return "", err
	}
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	return string(body), err
}

func stock(w http.ResponseWriter, r *http.Request) {
	plant := r.URL.Query().Get("plant")
	start := time.Now()
	answer, err := askSupplier(r.Context(), plant)
	if err != nil {
		log.Printf("%s: %v (%.1fs)", plant, err, time.Since(start).Seconds())
		http.Error(w, "supplier didn't answer", http.StatusGatewayTimeout)
		return
	}
	log.Printf("%s (%.1fs)", answer, time.Since(start).Seconds())
	fmt.Fprintln(w, answer)
}

func main() {
	log.SetFlags(0)
	http.HandleFunc("/stock", stock)
	log.Println("garden shop listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
