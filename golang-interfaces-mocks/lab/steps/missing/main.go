package main

import (
	"fmt"
	"net/http"
)

const pricePerDozen = 450 // cents

// Payer is anything that can take a payment.
type Payer interface {
	Charge(cents int) error
}

// CardReader is the card reader on Tom's egg stand.
type CardReader struct {
	URL string
}

// Charge asks the card service to take the money.
func (c CardReader) Charge(cents int) error {
	resp, err := http.Post(fmt.Sprintf("%s/charge?cents=%d", c.URL, cents), "text/plain", nil)
	if err != nil {
		return err
	}
	resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("card declined: %s", resp.Status)
	}
	return nil
}

// Sell charges for the eggs, then hands them over.
func Sell(p Payer, dozens int) (int, error) {
	if err := p.Charge(dozens * pricePerDozen); err != nil {
		return 0, err
	}
	return dozens * 12, nil
}

// CashBox is the honesty box for coins.
type CashBox struct {
	Total int
}

func (b *CashBox) Take(cents int) error {
	b.Total += cents
	return nil
}

func main() {
	card := CardReader{URL: "http://127.0.0.1:9000"}
	box := &CashBox{}
	eggs, err := Sell(card, 2)
	fmt.Println("card reader: eggs", eggs, "err", err)
	eggs, err = Sell(box, 1)
	fmt.Println("cash box:    eggs", eggs, "err", err, "box holds", box.Total)
}
