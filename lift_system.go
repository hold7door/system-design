// Problem Statement:
// Suppose a residential building has 30 floors and you are tasked to install an elevator system with 2 lifts. You need to design an algorithm for the elevator system such that the average wait time to get into the lift for any user is a minimum


// Expectation
// Pseudocode with the complete lift algorithm

// Assume the capacity is unlimited
// It can handle simultaneous requests and if the lift fails then other lift should take over all requests

package main

import (
  "fmt"
  "time"
  "sort"
  "slices"
)


type Elevator struct {
  currentFloor int
  requests []int
  direction int // 1 , -1
}


func NewElevator() *Elevator {
  return &Elevator{
    currentFloor: 3,
    direction: 1,
    requests: []int{},
  }
}


func (e *Elevator) RequestFloor(floor int) {
  fmt.Printf("Requested floor %d\n", floor)

  if !(e.direction == 1 && (floor > e.currentFloor && slices.Contains(e.requests, floor)) || (e.direction == -1 && (floor < e.currentFloor && slices.Contains(e.requests, floor)))) {
    e.requests = append(e.requests, floor)
  }

  fmt.Printf("requests %d\n", e.requests)

  // e.requests = append(e.requests, floor)
}

func (e *Elevator) ProcessRequests() {
    fmt.Printf("total request to process %d\n", len(e.requests))
    if (len(e.requests) == 0){
      // no requests to process
      return
    }

    if e.direction == 1 {
      sort.Ints(e.requests)
    } else {
      sort.Sort(sort.Reverse(sort.IntSlice(e.requests)))
    }
    fmt.Printf("Current requests %d\n", e.requests)

    // find next request to process
    // this is next request in current direction

    served := -1

    for idx, floor := range e.requests {
       if ((e.direction == 1 && floor >= e.currentFloor) || (e.direction == -1 && floor <= e.currentFloor)) {
          // found next floor
          time.Sleep(500 * time.Millisecond)
          e.currentFloor = floor
          fmt.Printf("Elevator reached floor %d \n", e.currentFloor)
          served = idx
          break
      }
    }

    if (served == -1){
      // no floor found current direction
      // change direction
      e.direction *= -1
    } else {
      // removed reached floor
      e.requests = slices.Delete(e.requests, served, served+1)
    }
}

func (e *Elevator) Start() {
    for true {
    e.ProcessRequests()
  }
}

func main(){
  elevator := NewElevator()
  fmt.Printf("Starting elevator at %d\n", elevator.currentFloor)

  go elevator.Start()

  // Example requests

  go func ()  {


	elevator.RequestFloor(5)
	elevator.RequestFloor(3)
	elevator.RequestFloor(7)
	elevator.RequestFloor(1)
	elevator.RequestFloor(4)
  elevator.RequestFloor(2)


	elevator.RequestFloor(5)
	elevator.RequestFloor(3)
	elevator.RequestFloor(7)
	elevator.RequestFloor(1)
	elevator.RequestFloor(4)
  elevator.RequestFloor(2)
 
  
	elevator.RequestFloor(5)
	elevator.RequestFloor(3)
	elevator.RequestFloor(7)
	elevator.RequestFloor(1)
	elevator.RequestFloor(4)
  elevator.RequestFloor(2)

  
	elevator.RequestFloor(5)
	elevator.RequestFloor(3)
	elevator.RequestFloor(7)
	elevator.RequestFloor(1)
	elevator.RequestFloor(4)
  elevator.RequestFloor(2)

  
	elevator.RequestFloor(5)
	elevator.RequestFloor(3)
	elevator.RequestFloor(7)
	elevator.RequestFloor(1)
	elevator.RequestFloor(4)
  elevator.RequestFloor(2)

}()
  time.Sleep(2500000 * time.Millisecond)

}

