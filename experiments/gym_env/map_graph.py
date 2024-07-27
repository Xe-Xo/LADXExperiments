## Creates a Live Graph (Nodes Edges not Plotting) of a Room for Analysis of Agent Movement

### TODO Fix the Screen / Warp Transitions to ensure we dont have world positions mid transfer.
#pip install igraph
import igraph as ig
import matplotlib.pyplot as plt



g = ig.Graph(directed=True)

vertex_dict = {}

def add_pos(g,x,y,z,color="grey"):
    vertex_dict[(x,y,z)] = g.add_vertex(real_name=(x,y,z), x=(x+z*13)*10, y=(y*10), color=color)

def add_transition(g : ig.Graph,x0,y0,z0,x1,y1,z1):
    g.add_edge(source=vertex_dict[(x0, y0, z0)], target=vertex_dict[(x1, y1, z1)])


for x in range(0, 12): # 10 X Coords + 2 Screen Edge
    for y in range(0, 10):
        add_pos(g, x,y,0, color="grey" if x != 0 and x != 11 and y != 0 and y != 9 else "pink")

# Add Staircase and Warps

add_pos(g, 0, 0, 1, color="red")
add_pos(g, 0, 1, 1, color="red")
add_pos(g, 0, 2, 1, color="red")
add_pos(g, 0, 7, 1, color="blue")

z = 0
for x in range(1, 11):
    for y in range(1, 9):
        for xp in [-1,0,1]:
            for yp in [-1,0,1]:
                if xp == 0 and yp == 0:
                    continue
                
                if x + xp >= 12:
                    continue
                if y + yp >= 10:
                    continue
                if x + xp < 0:
                    continue
                if y + yp < 0:
                    continue

                add_transition(g, x, y, z, x+xp, y+yp, z)


from igraph import summary

import random

to_remove = []

for vert in vertex_dict.values():
    if random.choice([True,False]) == False:
        to_remove.append(vert.index)
g.delete_vertices(to_remove) 


#g.vs["label"] = g.vs["real_name"] 

print(g.degree_distribution())

fig, ax = plt.subplots()
ig.plot(
    g,
    target=ax,
    layout="auto",
    vertex_size=10,
    #vertex_color="grey",
    edge_color="#222",
    edge_width=1,
    edge_arrow_size=0.01,
    margin=10,
    #vertex_label_size=2
)
plt.show()

