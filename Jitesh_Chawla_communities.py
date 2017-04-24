import sys
from collections import defaultdict
import community
import networkx as nx
import matplotlib.pyplot as plt
import operator


## Initializations

input_list = []
betweenness_dict = {}
value = 0
output_list = []
global_dict_connected_components = defaultdict(list)
modularity_dict = {}

## Taking output and input parameters from the console.
inputfile = str(sys.argv[1])
final_image = str(sys.argv[2])

## Reading the input file into a list(list of edges)
for line in open(inputfile):
    line = line.rstrip('\n')
    basket = line.split(' ')
    input_list.append(map(int,basket))

## Creating two copies of the original graph i.e G and G_final by using the nx.Graph() function on the input list
G = nx.Graph()
G_final = nx.Graph()
G.add_edges_from(input_list)
G_final.add_edges_from(input_list)

## Creating a list of color sequence corresponding to each of the nodes.
color_list = [] * G.number_of_nodes()


## Looping until there anre no more edges left in the input_list(list of edges) with the breaking condition on the input_list being empty
while (input_list):

    if not input_list:
        break
    else:
        ## Finding the edge betweeness among the edges using the nx.edge_betweenness_centrality() of networkxx and breaking the loop while
        ## when there is no corresponding edge found in the dictionary betweenness_dict{}

        betweenness_dict = nx.edge_betweenness_centrality(G, normalized=True, weight=None)

        if not betweenness_dict:
            break

        ## Calculating the edge with the maximum betweenness and removing the edge in the form of the key of the dictionary from the original graph
        max_betweenness_edge = max(betweenness_dict.iteritems(), key=operator.itemgetter(1))[0]
        G.remove_edge(*max_betweenness_edge)



        connected_components_list = []
        connected_components_set = []
        connected_components_set = sorted(nx.connected_components(G))


        ## Appending the list of lists of Connected components at each iteration
        for i in range(len(list(nx.connected_components(G)))):
            connected_components_list.append(list(connected_components_set[int(i)]))

        ## Also creating a global dictionary of connected components to be used later to print the output.
        global_dict_connected_components[value].append(connected_components_list)

        ## Appending a local dictionary which can be passed to the modularity function of the community at every iteration
        local_dict_connected_components = defaultdict(list)
        for val in range(len(connected_components_list)):
            for val2 in connected_components_list[val]:
                local_dict_connected_components[val2].append(val + 1)
        for k, v in local_dict_connected_components.iteritems():
            local_dict_connected_components[k] = v[0]
        local_dict_connected_components = dict(local_dict_connected_components)

        ## Constraint for finding the modularity i.e until number of edges in the graph re not zero
        if G.number_of_edges() != 0:
            temp = community.modularity(dict(local_dict_connected_components), G)
            modularity_dict[value] = temp
        connected_components_list = []
        value += 1


## Finding the maximum modularity of the particular connected component set and returning it.
max_modularity = max(modularity_dict.iteritems(), key=operator.itemgetter(1))[0]



## Printing the standard output -

for ele1 in dict(global_dict_connected_components)[max_modularity]:
    for ele2 in sorted(ele1):
        ele2 = [int(x) for x in ele2]
        output_list.append(sorted(ele2))
for result in output_list:
    print(result)

jc = 1
for jitesh in sorted(output_list):
    for chawla in jitesh:
        color_list.insert(chawla - 1, jc)
    jc += 1


## Plotting the final graph and saving it as "image.png"
nx.draw_networkx(G=G_final, pos=nx.fruchterman_reingold_layout(G_final),node_color=color_list, with_labels=True,cmap=plt.get_cmap('jet'))
plt.axis("off")
plt.savefig(final_image)