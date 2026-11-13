package main

import "github.com/gin-gonic/gin"

func main() {
	r := gin.Default()
	r.GET("/plants", listPlants)
	r.GET("/plants/:id", getPlant)

	staff := r.Group("/plants", requireKey)
	staff.POST("", createPlant)
	staff.PUT("/:id", updatePlant)
	staff.DELETE("/:id", deletePlant)

	r.Run(":8080")
}
