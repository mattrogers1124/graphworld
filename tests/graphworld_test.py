import matplotlib.pyplot as plt
from graphworld.graphworld import GraphWorld


def plot_graphworld(g: GraphWorld):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    xs, ys, zs = [], [], []

    for e in g.edges:
        v1 = g.vertices[min(e)]
        v2 = g.vertices[max(e)]
        xs = [v1[0], v2[0]]
        ys = [v1[1], v2[1]]
        zs = [v1[2], v2[2]]
        plt.plot(xs, ys, zs, 'c', linewidth=1)

    for v in g.vertices:
        xs.append(v[0])
        ys.append(v[1])
        zs.append(v[2])
    ax.scatter(xs, ys, zs)

    plt.show()

if __name__ == '__main__':
    g = GraphWorld.generate_labyrinth(50, 2)
    plot_graphworld(g)
