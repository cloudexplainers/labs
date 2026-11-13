package main

import "github.com/gin-gonic/gin"

func main() {
	r := gin.Default()
	r.GET("/plants", listPlants)
	r.GET("/plants/:id", getPlant)
	r.POST("/plants", createPlant)
	r.PUT("/plants/:id", updatePlant)
	r.DELETE("/plants/:id", deletePlant)
	r.Run(":8080")
}
