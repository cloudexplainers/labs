package main

import (
	"log"
	"os"

	"github.com/gin-gonic/gin"
)

func setupRouter(key string) *gin.Engine {
	r := gin.Default()
	r.GET("/plants", listPlants)
	r.GET("/plants/:id", getPlant)

	staff := r.Group("/plants", requireKey(key))
	staff.POST("", createPlant)
	staff.PUT("/:id", updatePlant)
	staff.DELETE("/:id", deletePlant)
	return r
}

func main() {
	key := os.Getenv("NURSERY_KEY")
	if key == "" {
		log.Fatal("NURSERY_KEY is not set")
	}
	setupRouter(key).Run(":8080")
}
