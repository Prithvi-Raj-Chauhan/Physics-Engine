# Physics Simulator

A small Python physics sandbox for experimenting with vectors, forces, motion, body updates, and simulation management. The project is built as a lightweight engine package with simple scripts that demonstrate the current workflow.

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
4. `engine.physics.Engine` manages bodies and steps the simulation forward.
5. `main.py` and `test.py` act as small manual experiments for checking how forces, impulses, and engine updates affect a body.

This is a clean workflow for a physics engine because each layer depends on the simpler layer below it. Vectors come first, then constants, then bodies, then the engine that coordinates those bodies.

## Vector System

`Vector` stores `x`, `y`, and `z` components and supports:

- vector addition with `+`
- scalar multiplication from either side, such as `v * 3` or `3 * v`
- negative scalar multiplication, such as `-1 * v`
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

Forces are applied using Newton's second law. `Body.applyforce(force)` converts force into acceleration and adds it to the body's current acceleration:

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

`Body.releaseForce(force)` removes a previously applied force by applying the opposite force. `Body.impulse(force, time)` applies a force, updates the body for a duration, and then releases that same force.

## Engine

`Engine` is the simulation manager. Instead of updating every body manually in a script, you add bodies to the engine and let the engine update them together.

Current responsibilities:

- store all simulated bodies in `self.bodies`
- add bodies with `addBody`
- apply gravity to every body with `applyGravity`
- update every body with `update(dt)`

Basic usage:

```python
from engine.bodies import Body
from engine.physics import Engine
from engine.vectors import Vector

ball = Body(100, Vector(), Vector())

engine = Engine()
engine.addBody(ball)
engine.applyGravity()

for _ in range(1, 10):
    engine.update(1)
    print(ball.pos)
```

The engine currently applies gravity once by adding `gr * body.mass` as a force to each body. Since `Body.applyforce` accumulates acceleration, the body keeps that acceleration during later updates.

## Example Scripts

`main.py` shows a short impulse-style test:

```python
BODY = Body(1, Vector(3, 4, 0))
BODY.impulse(Vector(1, 0, 0), 2)
```

`test.py` shows the engine workflow:

```python
ENGINE = Engine()
ENGINE.addBody(ball)
ENGINE.applyGravity()
ENGINE.update(1)
```

It creates a body, registers it with the engine, applies gravity once, and then updates the simulation once per second.

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
- then adding an engine to manage bodies together
- then running small scripts that apply forces through the body or engine and print positions over time

That is a sensible early-engine workflow because the math stays visible and easy to debug while the responsibility of each class stays clear.

## Approach Analysis

The current design has a useful separation of concerns:

- `Vector` handles math.
- `Body` handles physical state and motion.
- `Engine` handles groups of bodies and global simulation updates.

This is the right direction because the engine does not need to know the details of the motion equation. It only tells each body to update. That keeps the simulation manager simple and makes it easier to add more bodies later.

The gravity approach is also physically meaningful:

```python
force = gravity * body.mass
acceleration = force / body.mass
```

So every body gets the same gravitational acceleration no matter its mass, which matches real-world gravity when air resistance is ignored.

## What Can Be Improved

- Add `__sub__`, `__truediv__`, and equality support to `Vector`.
- Add type hints consistently across all methods.
- Avoid using `Vector()` as a default argument in `Body.__init__`; use `None` and create a new vector inside the constructor.
- Rename methods to standard Python style, such as `apply_force` and `release_force`.
- Consider renaming `addBody` to `add_body` to match Python naming conventions.
- Track simulation time inside `Engine`, for example `self.time += dt`.
- Add `remove_body` when you start deleting objects from the world.
- Add a `clear_forces` or acceleration reset workflow if you want temporary forces that last only one frame.
- Add unit tests for vector operations, force application, impulse, and position updates.
- Keep `test.py` tracked if it is meant to be an example, or move examples into an `examples/` folder.
- Add collision detection later, after the motion engine is stable.

## Next Engine Upgrade

Your current `Engine` is a solid first version. The next useful upgrade is to make gravity a property of the engine and apply it automatically during each update:

```python
from engine.constants import gr

class Engine:
    def __init__(self, gravity=gr):
        self.bodies = []
        self.gravity = gravity
        self.time = 0

    def addBody(self, body):
        self.bodies.append(body)

    def update(self, dt):
        for body in self.bodies:
            if self.gravity is not None:
                body.applyforce(self.gravity * body.mass)
            body.update(dt)
            body.releaseForce(self.gravity * body.mass)
        self.time += dt
```

This version treats gravity as a per-step force. It applies gravity, updates the body, and then releases gravity so acceleration does not accidentally grow if `applyGravity` or `update` is called multiple times.

After that, the engine can grow into springs, drag, collisions, and user-controlled forces without changing the basic project structure.
