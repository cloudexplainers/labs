package main

import "testing"

func TestSell(t *testing.T) {
	card := CardReader{URL: "http://127.0.0.1:9000"}
	eggs, err := Sell(card, 2)
	if err != nil {
		t.Fatal(err)
	}
	if eggs != 24 {
		t.Errorf("got %d eggs, want 24", eggs)
	}
}
