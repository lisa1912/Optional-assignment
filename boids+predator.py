"""
@author: Lisa Pijpers (15746704)

Boids assignment for the course Complex System Simulation
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set seed to make result reproducable
np.random.seed(100)

class Boid:
    def __init__(self, x, y):
        self.position = np.array([x, y])
        self.velocity = np.random.randn(2)
        self.acceleration = np.zeros(2)

class Predator:
    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=np.float64) 
        self.velocity = np.random.randn(2)

class Flock:
    def __init__(self, n, predator):
        self.boids = [Boid(np.random.rand()*100, np.random.rand()*100) for _ in range(n)]
        self.predator = predator

    def apply_rules(self):
        
        # Set perception radius for each rule
        separation_radius = 40
        alignment_radius = 20
        cohesion_radius = 50
        avoid_predator_radius = 30

        # Set weight for each rule
        separation_weight = 0.8
        alignment_weight = 0.06
        cohesion_weight = 0.07
        avoid_predator_weight = 1.5

        for boid in self.boids:
            separation = np.zeros(2)
            alignment = np.zeros(2)
            cohesion = np.zeros(2)
            avoid_predator = np.zeros(2)
            
            separation_total = 0
            alignment_total = 0
            cohesion_total = 0

            for other in self.boids:
                if np.all(boid.position != other.position):
                    boid_distance = np.linalg.norm(boid.position - other.position)

                    # Separation
                    if boid_distance < separation_radius:
                        separation += (boid.position - other.position) / boid_distance
                        separation_total += 1

                    # Alignment 
                    if boid_distance < alignment_radius:
                        alignment += other.velocity
                        alignment_total += 1

                    # Cohesion 
                    if boid_distance < cohesion_radius:
                        cohesion += other.position
                        cohesion_total += 1

            # Avoid predator
            predator_distance = np.linalg.norm(boid.position - self.predator.position)
            if predator_distance < avoid_predator_radius:
                avoid_predator += (boid.position - self.predator.position) / predator_distance

            if separation_total > 0:
                separation /= separation_total
            if alignment_total > 0:
                alignment /= alignment_total
            if cohesion_total > 0:
                cohesion /= cohesion_total
                cohesion = (cohesion - boid.position)

            boid.acceleration = (separation_weight * separation + alignment_weight * alignment + cohesion_weight * cohesion + avoid_predator_weight * avoid_predator)

    def update(self):
        self.apply_rules()
        for boid in self.boids:
            boid.velocity += boid.acceleration
            boid.position += boid.velocity

            # Periodic boundary conditions boids
            boid.position[0] = boid.position[0] % 100 
            boid.position[1] = boid.position[1] % 100 

            # Speed limit boids
            max_speed = 6
            speed = np.linalg.norm(boid.velocity)
            if speed > max_speed:
                boid.velocity = boid.velocity / speed * max_speed

        # Change direction of predator
        if np.random.rand() < 0.05:
            self.predator.velocity = np.random.randn(2)
        self.predator.position += self.predator.velocity / np.linalg.norm(self.predator.velocity)
       
        # Periodic boundary conditions predator
        self.predator.position[0] = self.predator.position[0] % 100
        self.predator.position[1] = self.predator.position[1] % 100



def draw_boids(frame):
    flock.update()

    # Clear plot
    ax.clear()
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.xticks([], [])
    plt.yticks([], [])
    plt.title("Flocking of birds and a predator (red dot)", size=16)
    
    # Draw boids
    positions = np.array([boid.position for boid in flock.boids])
    velocities = np.array([boid.velocity for boid in flock.boids])

    velocities_new = velocities / (np.linalg.norm(velocities, axis=1, keepdims=True))

    ax.quiver(positions[:, 0], positions[:, 1], velocities_new[:, 0], velocities_new[:, 1], angles="xy", scale_units="xy", scale=0.5, width=0.005, color="black")
    
    # Draw predator
    ax.scatter(flock.predator.position[0], flock.predator.position[1], color="red", s=50)


predator = Predator(50, 50)
flock = Flock(50, predator)

# Make animation
fig, ax = plt.subplots()
plt.xticks([], [])
plt.yticks([], [])

ax.set_facecolor("skyblue")
animation = FuncAnimation(fig, draw_boids, frames=200, interval=50)
plt.show()
