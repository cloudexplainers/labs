package main

import "github.com/gin-gonic/gin"

func main() {
	r := gin.Default()
	r.GET("/plants", listPlants)
	r.GET("/plants/:id", getPlant)
	r.Run(":8080")
}
