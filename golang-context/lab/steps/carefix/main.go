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
	ctx, cancel := context.WithTimeout(r.Context(), 3*time.Second)
	defer cancel()
	answer, err := askSupplier(ctx, plant)
	if err != nil {
		log.Printf("%s: %v (%.1fs)", plant, err, time.Since(start).Seconds())
		http.Error(w, "supplier didn't answer", http.StatusGatewayTimeout)
		return
	}
	log.Printf("%s (%.1fs)", answer, time.Since(start).Seconds())
	fmt.Fprintln(w, answer)
}

func careSheet(ctx context.Context, plant string) error {
	for page := 1; page <= 5; page++ {
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-time.After(time.Second): // slow work: one page
		}
		log.Printf("%s: care page %d", plant, page)
	}
	return nil
}

func care(w http.ResponseWriter, r *http.Request) {
	plant := r.URL.Query().Get("plant")
	start := time.Now()
	if err := careSheet(r.Context(), plant); err != nil {
		log.Printf("%s: %v (%.1fs)", plant, err, time.Since(start).Seconds())
		return
	}
	log.Printf("%s: care sheet done (%.1fs)", plant, time.Since(start).Seconds())
	fmt.Fprintln(w, "care sheet ready")
}

func main() {
	log.SetFlags(0)
	http.HandleFunc("/stock", stock)
	http.HandleFunc("/care", care)
	log.Println("garden shop listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
