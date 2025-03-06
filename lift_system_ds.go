package main

import (
	"fmt"
	"sort"
	"slices"
	"time"
)

type Elevator struct {
	currentFloor int
	requests     []int
	direction    int // 1 for up, -1 for down
	requestChan  chan int
	stopChan     chan struct{}
}

func NewElevator() *Elevator {
	return &Elevator{
		currentFloor: 3,
		direction:    1,
		requests:     []int{},
		requestChan:  make(chan int),
		stopChan:     make(chan struct{}),
	}
}

func (e *Elevator) RequestFloor(floor int) {
	fmt.Printf("Requested floor %d\n", floor)
	e.requestChan <- floor
}

func (e *Elevator) Start() {
	go func() {
		for {
			select {
			case floor := <-e.requestChan:
				// Add the request to the queue if it doesn't already exist
				if !slices.Contains(e.requests, floor) {
					e.requests = append(e.requests, floor)
					fmt.Printf("Added floor %d to requests. Current requests: %v\n", floor, e.requests)
				}
			case <-e.stopChan:
				fmt.Println("Elevator stopped.")
				return
			default:
				e.ProcessRequests()
			}
		}
	}()
}

func (e *Elevator) Stop() {
	close(e.stopChan)
}

func (e *Elevator) ProcessRequests() {
	if len(e.requests) == 0 {
		// No requests to process
		return
	}

	// Sort requests based on direction
	if e.direction == 1 {
		sort.Ints(e.requests)
	} else {
		sort.Sort(sort.Reverse(sort.IntSlice(e.requests)))
	}

	// Find the next floor to serve
	servedIdx := -1
	for idx, floor := range e.requests {
		if (e.direction == 1 && floor >= e.currentFloor) || (e.direction == -1 && floor <= e.currentFloor) {
			// Move to the next floor
			time.Sleep(500 * time.Millisecond) // Simulate time taken to move between floors
			e.currentFloor = floor
			fmt.Printf("Elevator reached floor %d\n", e.currentFloor)
			servedIdx = idx
			break
		}
	}

	if servedIdx == -1 {
		// No floors in the current direction, change direction
		e.direction *= -1
		fmt.Printf("Changing direction to %d\n", e.direction)
	} else {
		// Remove the served floor from the requests
		e.requests = slices.Delete(e.requests, servedIdx, servedIdx+1)
	}
}

func main() {
	elevator := NewElevator()
	fmt.Printf("Starting elevator at floor %d\n", elevator.currentFloor)

	elevator.Start()

	// Example requests
	go func() {
		elevator.RequestFloor(5)
		time.Sleep(200 * time.Millisecond)
		elevator.RequestFloor(3)
		time.Sleep(200 * time.Millisecond)
		elevator.RequestFloor(7)
		time.Sleep(200 * time.Millisecond)
		elevator.RequestFloor(1)
		time.Sleep(200 * time.Millisecond)
		elevator.RequestFloor(4)
		time.Sleep(200 * time.Millisecond)
		elevator.RequestFloor(2)
	}()

	// Let the elevator run for a while
	time.Sleep(10 * time.Second)
	elevator.Stop()
}
