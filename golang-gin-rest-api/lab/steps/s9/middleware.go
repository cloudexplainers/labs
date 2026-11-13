package main

import (
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

func requireKey(c *gin.Context) {
	if c.GetHeader("X-API-Key") != os.Getenv("NURSERY_KEY") {
		c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing or wrong API key"})
		return
	}
	c.Next()
}
