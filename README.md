# Physics Simulator

A small Python physics sandbox for experimenting with vectors, forces, motion, and body updates. The project is currently built as a lightweight engine package plus a couple of simple scripts that demonstrate how the pieces work together.

## Project Structure

```text
Physics/
+-- engine/
|   +-- __init__.py
|   +-- bodies.py
|   +-- constants.py
|   +-- physics.py
|   +-- vectors.py
+-- main.py
+-- test.py
+-- .gitignore
```

## Core Ideas

The simulator is organized in layers:

1. `engine.vectors.Vector` provides the basic 3D vector type.
2. `engine.constants` defines reusable physics constants as vectors or numbers.
3. `engine.bodies.Body` represents a physical object with mass, position, velocity, acceleration, and momentum.
4. `main.py` and `test.py` act as small manual experiments for checking how forces and updates affect a body.

This is a good workflow for a physics engine because each layer depends on the simpler layer below it. Vectors come first, then constants, then bodies, then simulation behavior.

## Vector System

`Vector` stores `x`, `y`, and `z` components and supports:

- vector addition with `+`
- scalar multiplication from either side, such as `v * 3` or `3 * v`
- dot product with `dot`
- magnitude with `mag`
- readable printing through `__repr__`

Example:

```python
from engine.vectors import Vector

a = Vector(2, 3, 0)
b = Vector(1, 0, 2)

print(a + b)
print(a * 3)
print(a.dot(b))
```

## Constants

`engine.constants` defines common values:

```python
g = Vector(y=-9.8)
gr = Vector(y=-10)
G = 6.67e-11
```

`g` and `gr` are gravity-style acceleration vectors. `G` is the universal gravitational constant.

## Bodies

`Body` is the main object currently being simulated.

Each body stores:

- `mass`
- `pos`
- `vel`
- `acc`
- `momentum`

Forces are applied using Newton's second law:

```python
acceleration = force / mass
```

The `update(time)` method advances the body using constant-acceleration motion:

```python
position += velocity * time + 0.5 * acceleration * time * time
velocity += acceleration * time
momentum = mass * velocity
```

Basic usage:

```python
from engine.bodies import Body
from engine.vectors import Vector

ball = Body(10, Vector(), Vector(30, 40, 0))
gravity = Vector(y=-100)

ball.applyforce(gravity)
ball.update(1)

print(ball.pos)
```

## Example Scripts

`main.py` shows a short impulse-style test:

```python
BODY = Body(1, Vector(3, 4, 0))
BODY.impulse(Vector(1, 0, 0), 2)
```

`test.py` creates a body, applies gravity and then another horizontal force, then updates the body once per second for eight seconds. With the current `Body.applyforce` behavior, the second force replaces the first one, so this script also exposes why force accumulation would be useful.

Run either script with:

```bash
python main.py
python test.py
```

## Current Workflow

The project is being developed by testing each concept manually:

- first checking vector arithmetic
- then defining constants
- then adding body motion
- then running small scripts that apply forces and print positions over time

That is a sensible early-engine workflow because the math stays visible and easy to debug before adding a larger simulation manager.

## What Can Be Improved

- Add `__sub__`, `__truediv__`, and equality support to `Vector`.
- Add type hints consistently across all methods.
- Avoid using `Vector()` as a default argument in `Body.__init__`; use `None` and create a new vector inside the constructor.
- Rename methods to standard Python style, such as `apply_force` and `release_force`.
- Add unit tests for vector operations, force application, impulse, and position updates.
- Keep `test.py` tracked if it is meant to be an example, or move examples into an `examples/` folder.
- Add collision detection later, after the motion engine is stable.

## Suggested Engine Class

The `Engine` class should manage the whole simulation instead of making every script update bodies manually.

Its main jobs should be:

- store all bodies in the simulation
- store global forces such as gravity
- apply global forces to each body
- step the simulation forward by `dt`
- optionally track simulation time

A simple first version could look like this:

```python
class Engine:
    def __init__(self, gravity=None):
        self.bodies = []
        self.gravity = gravity
        self.time = 0

    def add_body(self, body):
        self.bodies.append(body)

    def step(self, dt):
        for body in self.bodies:
            if self.gravity is not None:
                body.applyforce(self.gravity * body.mass)
            body.update(dt)
        self.time += dt
```

After that works, improve it by accumulating forces per body:

```python
body.add_force(force)
body.clear_forces()
```

Then the engine can calculate net force once per step, update acceleration, advance motion, and clear the forces for the next frame. That will make the simulator easier to extend with gravity, thrust, springs, drag, collisions, and user-controlled forces.
