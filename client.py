from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from noise import pnoise2
import numpy as np

# Map dimensions
map_width, map_height = 100, 100
scale = 50.0

# Generate Perlin noise map
def generate_perlin_noise_map(width, height, scale):
    map = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            map[i][j] = pnoise2(i / scale, j / scale, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=42)
    return map

noise_map = generate_perlin_noise_map(map_width, map_height, scale)

app = Ursina()

# Create blocks based on the noise map
for i in range(map_width):
    for j in range(map_height):
        if noise_map[i][j] > 0.1:
            block_type = 'grass'  # Land
        else:
            block_type = 'water'  # Water

        # Create a cube for each block
        cube = Entity(model='cube', texture=block_type, position=(i, noise_map[i][j], j))

# Spawn the player on top of the terrain
player = FirstPersonController(y=np.max(noise_map) + 1)

def update():
    # Make the player stick to the surface
    player.y = noise_map[int(player.x)][int(player.z)] + 1

app.run()
