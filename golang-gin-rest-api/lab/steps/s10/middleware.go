package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func requireKey(key string) gin.HandlerFunc {
	return func(c *gin.Context) {
		if c.GetHeader("X-API-Key") != key {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing or wrong API key"})
			return
		}
		c.Next()
	}
}
