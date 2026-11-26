package main

import "testing"

func BenchmarkGrow(b *testing.B) {
	for b.Loop() {
		grow(10000)
	}
}

func BenchmarkPresized(b *testing.B) {
	for b.Loop() {
		presized(10000)
	}
}
