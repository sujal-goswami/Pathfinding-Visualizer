# Pathfinding-Visualizer

<div align="center">
    <img src="https://github.com/sujal-goswami/Pathfinding-Visualizer/blob/main/Demo.gif" width="500" height="500">
</div>  

&nbsp;  

>  Press  **left click** -> source, destination, obstacles
>  
>  Press **right click** -> clear spot 
>  
>  Press **Ctrl+C** -> restart program 
>  
>  Press **Space** -> Start algorithm  

## What is the A* Algorithm and how does it work?
A* (pronounced "A-star") is a popular pathfinding algorithm used to find the shortest path between two points in a graph. It is both complete (guaranteed to find a solution if one exists) and optimal (guaranteed to find the shortest path).

Here's a step-by-step explanation of how the A* algorithm works using an example of finding the shortest path in a grid-based graph:

1. Initialize the algorithm:<br>
    - Define the start and goal nodes.
    - Create an open set to store nodes that need to be evaluated.
    - Create a closed set to store nodes that have been evaluated.
    - Assign tentative distances to all nodes. Initially, set the distance of the start node to 0 and the distance of all other nodes to infinity.
    - Assign a heuristic value to each node, representing the estimated cost from that node to the goal. This heuristic guides the algorithm towards the goal. In this example, we'll use the Manhattan distance as the heuristic.
2. Start the algorithm:
    - Add the start node to the open set.
3. Iterate until the open set is empty or the goal is reached:
    - Select the node with the lowest total cost (f-score) from the open set. This node becomes the current node.
    - If the current node is the goal, the algorithm has found the shortest path. Reconstruct the path from the goal to the start using the "came from" data structure.
    - Move the current node from the open set to the closed set to mark it as evaluated.
    - Explore the neighbors of the current node:
        - For each neighbor, calculate the tentative g-score, which is the cost to move from the start node to the neighbor through the current node. If the g-score is lower than the neighbor's current g-score, update it.
        - Calculate the f-score of the neighbor by adding the g-score and the heuristic value.
        - If the neighbor is not in the open set, add it and mark the current node as its "came from" node. Otherwise, if the neighbor is already in the open set but has a higher g-score, skip it.
4. If the open set becomes empty and the goal has not been reached, there is no path from the start to the goal. <br>

Note: In the given code example, the A* algorithm is implemented to find the shortest path in a grid-based graph, where the nodes represent spots on the grid. The algorithm uses a priority queue (PriorityQueue) to efficiently process nodes with the lowest f-score first.      

## Why did I select A* Alogritm ?

 In order to find the path, an algorithm A* has been selected in view of the following reasons:
 
 1. Completeness: A* guarantees to find a solution if one exists.
 2. Optimality: A* finds the shortest path between the start and goal nodes.
 3. Heuristic function: A* uses the Manhattan distance heuristic, which estimates the remaining distance to the goal and improves efficiency.
 4. Efficiency: A* efficiently explores the graph using a balanced search strategy.
 5. Versatility: A* can be applied to various graph types and domains.

## Real life use cases

1. Navigation Systems: The program can be used in navigation systems to find the shortest path between two locations on a map. It can help drivers, pedestrians, or delivery services determine the most efficient route to reach their destination.
2. Robotics: The program can be utilized in robotics for path planning and obstacle avoidance. Robots can use the A* algorithm to navigate through complex environments while avoiding obstacles, ensuring efficient and safe movement.
3. Game Development: The program can be employed in game development to create intelligent and efficient enemy AI or non-player characters (NPCs). It enables NPCs to find their way through game levels, solve mazes, or chase players using the shortest path.
4. Network Routing: The program can be applied in network routing protocols to determine optimal paths for data packets to traverse a network. It helps in minimizing latency and maximizing data transfer efficiency in computer networks.
5. Supply Chain Optimization: The program can be used in supply chain management to optimize logistics and transportation routes. It can help determine the most efficient path for delivering goods, reducing costs, and improving delivery times.
6. Robot Path Planning in Manufacturing: The program can be utilized in industrial automation to plan paths for robots in manufacturing processes. It helps in optimizing the movement of robots, improving productivity, and reducing collision risks.












