package main

import (
	"net/http"
	"slices"
	"strconv"

	"github.com/gin-gonic/gin"
)

func listPlants(c *gin.Context) {
	light := c.Query("light")
	list := []Plant{}
	for _, p := range plants {
		if light == "" || p.Light == light {
			list = append(list, p)
		}
	}
	slices.SortFunc(list, func(a, b Plant) int { return a.ID - b.ID })
	c.JSON(http.StatusOK, list)
}

func getPlant(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "id must be a number"})
		return
	}
	p, ok := plants[id]
	if !ok {
		c.JSON(http.StatusNotFound, gin.H{"error": "plant not found"})
		return
	}
	c.JSON(http.StatusOK, p)
}

type NewPlant struct {
	Name  string `json:"name" binding:"required"`
	Light string `json:"light" binding:"required,oneof=sun shade"`
	Stock int    `json:"stock" binding:"min=0"`
}

func createPlant(c *gin.Context) {
	var in NewPlant
	if err := c.ShouldBindJSON(&in); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	nextID++
	p := Plant{ID: nextID, Name: in.Name, Light: in.Light, Stock: in.Stock}
	plants[p.ID] = p
	c.JSON(http.StatusCreated, p)
}

func updatePlant(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "id must be a number"})
		return
	}
	if _, ok := plants[id]; !ok {
		c.JSON(http.StatusNotFound, gin.H{"error": "plant not found"})
		return
	}
	var in NewPlant
	if err := c.ShouldBindJSON(&in); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	p := Plant{ID: id, Name: in.Name, Light: in.Light, Stock: in.Stock}
	plants[id] = p
	c.JSON(http.StatusOK, p)
}

func deletePlant(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "id must be a number"})
		return
	}
	if _, ok := plants[id]; !ok {
		c.JSON(http.StatusNotFound, gin.H{"error": "plant not found"})
		return
	}
	delete(plants, id)
	c.Status(http.StatusNoContent)
}
