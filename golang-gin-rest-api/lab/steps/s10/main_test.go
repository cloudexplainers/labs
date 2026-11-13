package main

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"
)

func TestMain(m *testing.M) {
	gin.SetMode(gin.TestMode)
	m.Run()
}

func TestGetPlant(t *testing.T) {
	r := setupRouter("test-key")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, httptest.NewRequest("GET", "/plants/1", nil))
	if w.Code != http.StatusOK || !strings.Contains(w.Body.String(), `"name":"Fern"`) {
		t.Fatalf("got %d %s", w.Code, w.Body.String())
	}
}

func TestMissingPlant(t *testing.T) {
	r := setupRouter("test-key")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, httptest.NewRequest("GET", "/plants/99", nil))
	if w.Code != http.StatusNotFound {
		t.Fatalf("got %d, want 404", w.Code)
	}
}

func TestCreateNeedsKey(t *testing.T) {
	r := setupRouter("test-key")
	w := httptest.NewRecorder()
	body := strings.NewReader(`{"name":"Mint","light":"sun","stock":5}`)
	r.ServeHTTP(w, httptest.NewRequest("POST", "/plants", body))
	if w.Code != http.StatusUnauthorized {
		t.Fatalf("got %d, want 401", w.Code)
	}
}

func TestBadID(t *testing.T) {
	r := setupRouter("test-key")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, httptest.NewRequest("GET", "/plants/abc", nil))
	want := `{"error":"id must be a number"}`
	if w.Code != http.StatusBadRequest || w.Body.String() != want {
		t.Fatalf("got %d %s, want 400 %s", w.Code, w.Body.String(), want)
	}
}
