# GraphWorld Initial Design Notes

We want to procedurally generate a world
for use in exploration and strategy games.
Here are some concrete examples of
what we're aiming to implement abstractly:

> A strategy game that takes place in a fantasy setting.
> The world map is a globe, subdivided into geographic regions
> like plains, desert, ocean, mountain range, and so on.
> Travel is possible between adjacent regions.

> An exploration game that takes place in a sci-fi setting.
> The player is captain of a ship that's exploring the galaxy.
> The galaxy map consists of points on the celestial sphere,
> like star systems, black holes, nebulas, and so on.
> Adjacent regions are connected by wormholes.

Here's the abstract version,
using the language of graph theory.

> A graph, *G*, with vertex set *V* and edge set *G*.
> Vertices have coordinates in **R**<sup>3</sup>,
> all on the unit sphere.
> Edges connect vertices that are close to each other
> with respect to this coordinate system.

### Implementation

Let *n* be the number of vertices.
Index the vertices as
*v*<sub>0</sub>, *v*<sub>1</sub>, ... , *v*<sub>*n*-1</sub>.

An instance of `GraphWorld` has the following properties:

* `vertices: list` - List of length *n*.
The entries are the coordinates of
*v*<sub>0</sub>, *v*<sub>1</sub>, ... , *v*<sub>*n*-1</sub>,
stored as 3-tuples of floats.

* `edges: set` - Set of edges.
An edge is represented as a frozenset containing two integers,
which are the indices of the adjacent vertices.

* `neighbors: dict` - Dict whose keys are in `range(n)`.
The corresponding value `neighbors[i]` is a set,
containing indices of vertices adjacent to *v*<sub>*i*</sub>.

And that's it.
Note that both the `edges` and `neighbors` properties
encode the same information two different ways.
We'll need to implement an API to ensure these stay consistent:

* `add_edge(self, index1, index2)` - Add an edge
connecting the two vertices whose indices were passed in.
If the edge already exists, do nothing.
If the arguments are invalid, raise an exception.

* `remove_edge(self, index1, index2)` - Remove any edge
connecting the two vertices whose indices were passed in.
If the edge doesn't exist, do nothing.
If the arguments are invalid, raise an exception.

A static factory method, `generate(n, alpha)`,
returns a new object of type `GraphWorld` with *n* vertices.
The argument *alpha* is used in generation, described below.