package main

import (
	"errors"
	"testing"
)

// fakePayer stands in for the card reader in tests: no network, no real card.
type fakePayer struct {
	charged []int
	err     error
}

func (f *fakePayer) Charge(cents int) error {
	f.charged = append(f.charged, cents)
	return f.err
}

func TestSellCharges(t *testing.T) {
	fake := &fakePayer{}
	eggs, err := Sell(fake, 2)
	if err != nil || eggs != 24 {
		t.Fatalf("got %d eggs, err %v", eggs, err)
	}
	if len(fake.charged) != 1 || fake.charged[0] != 900 {
		t.Errorf("charged %v, want [900]", fake.charged)
	}
}

func TestSellDeclined(t *testing.T) {
	fake := &fakePayer{err: errors.New("card declined")}
	eggs, err := Sell(fake, 2)
	if err == nil {
		t.Fatal("want an error")
	}
	if eggs != 0 {
		t.Errorf("handed over %d eggs for a declined card", eggs)
	}
}
