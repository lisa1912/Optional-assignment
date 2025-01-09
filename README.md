# Optional programming assignment (Boids)
This code visualizes a simple flocking simulation based on Craig Reynolds' Boids model. It simulates the movement of birds (boids) as they interact with each other and avoid a predator. The simulation is visualized using Matplotlib. 

## **Features**
Rules for the boids:
- Separation
- Alignment
- Cohesion
- Avoid predator

## **Usage**
Run the simulation. The simulation will open a window displaying the flocking behavior of the boids and the predator. The boids are represented as arrows, while the predator is represented as a red dot.
1. Boid movement: Each boid calculates its acceleration based on the rules of separation, alignment, cohesion, and avoiding the predator.
2. Predator movement: The predator randomly changes its direction and moves across the screen.
3. Boundary conditions: Both the boids and the predator have periodic boundary conditions.
