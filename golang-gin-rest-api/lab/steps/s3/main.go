package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type Plant struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Light string `json:"light"`
	Stock int    `json:"stock"`
}

var plants = []Plant{
	{1, "Fern", "shade", 12},
	{2, "Basil", "sun", 40},
	{3, "Olive tree", "sun", 2},
}

func main() {
	r := gin.Default()
	r.GET("/plants", func(c *gin.Context) {
		c.JSON(http.StatusOK, plants)
	})
	r.Run(":8080")
}
