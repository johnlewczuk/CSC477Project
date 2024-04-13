#!/usr/bin/python
from common import *

class FastRRTPlanner(RRTPlanner):
    """
    Implementation of the Fast RRT* Planning algorithm.
    """

    def plan(self, start_state, dest_state, max_num_steps, max_steering_radius, hybrid_lambda, test, filename):
        """
        Returns a path as a sequence of states [start_state, ..., dest_state]
        if dest_state is reachable from start_state. Otherwise returns [start_state].
        Assume both source and destination are in free space.
        """
        assert (self.state_is_free(start_state))
        assert (self.state_is_free(dest_state))

        # The set containing the nodes of the tree
        tree_nodes = set()
        tree_nodes.add(start_state)

        # image to be used to display the tree
        img = np.copy(self.world)

        plan = [start_state]

        prev_sample = start_state

        for step in range(max_num_steps):

            s_rand = self.hybrid_sample(dest_state, prev_sample, hybrid_lambda)
            s_nearest = self.find_closest_state(tree_nodes, s_rand)
            s_new = self.steer_towards(s_nearest, s_rand, max_steering_radius)

            near_nodes = self.near(s_new, tree_nodes, max_steering_radius)
            s_parent = self.improved_choose_parent(s_new, near_nodes, s_nearest)

            if self.path_is_obstacle_free(s_parent, s_new):

                # Update parent and cost here
                s_new.parent = s_parent
                s_new.cost += s_parent.cost + s_new.euclidean_distance(s_parent)

                tree_nodes.add(s_new)
                s_parent.children.append(s_new)

                if self.path_is_obstacle_free(s_new, dest_state):
                    dest_state.parent = s_new
                    plan = self._follow_parent_pointers(dest_state)
                    break

                # plot the new node and edge
                cv2.circle(img, (s_new.x, s_new.y), 2, (0,0,0))
                cv2.line(img, (s_parent.x, s_parent.y), (s_new.x, s_new.y), (255,0,0))
            
                prev_sample = s_new
        

            # Keep showing the image for a bit even
            # if we don't add a new node and edge
            if (test == False):
                cv2.imshow('image', img)
                cv2.waitKey(10)
        
        if (plan == [start_state]):
            print("Fast-RRT: No path found!")
            return (None, -1, -1)
        
        if (filename != None):
            draw_plan_and_save(img, plan, [], filename, bgr=(0,0,255), thickness=2)

        if (test == False):
            draw_plan(img, plan, bgr=(0,0,255), thickness=2)
            cv2.waitKey(0)

        # Calculaute optimal path cost
        cost_of_optimal_path = 0
        curr_node = dest_state
        while curr_node.parent != None:
            cost_of_optimal_path += curr_node.euclidean_distance(curr_node.parent)
            curr_node = curr_node.parent
        
        return (plan, cost_of_optimal_path, len(tree_nodes))



if __name__ == "__main__":
        
    # world = cv2.imread('./worlds/simple_maze.png')
    # start_state = State(40, 40, None)
    # dest_state = State(1000, 650, None)

    # world = cv2.imread('./worlds/complex_maze.png')
    # start_state = State(40, 40, None)
    # dest_state = State(1000, 650, None)
        
    # world = cv2.imread('./worlds/complex_maze_concave.png')
    # start_state = State(160, 70, None)
    # dest_state = State(1000, 650, None)

    # world = cv2.imread('./worlds/cluttered.png')
    # start_state = State(40, 40, None)
    # dest_state = State(1000, 650, None)

    # world = cv2.imread('./worlds/floor_plan.png')
    # start_state = State(70, 860, None)
    # dest_state = State(1260, 100, None)
    # dest_state = State(1250, 850, None)

    # world = cv2.imread('./worlds/floor_plan_cleaned.png')
    # start_state = State(80, 820, None)
    # dest_state = State(1210, 90, None)
    # dest_state = State(1070, 800, None)

    # world = cv2.imread('./worlds/regular.png')
    # start_state = State(30, 25, None)
    # dest_state = State(925, 720, None)

    # world = cv2.imread('./worlds/irregular.png')
    # start_state = State(40, 35, None)
    # dest_state = State(800, 645, None)

    # world = cv2.imread('./worlds/narrow.png')
    # start_state = State(35, 35, None)
    # dest_state = State(1125, 900, None)

    world = cv2.imread('./worlds/sauga_map.png')
    start_state = State(0, 0, None)
    dest_state = State(4650, 4650, None)

    # world = cv2.imread('./worlds/sauga_map_resized.png')
    # start_state = State(10, 47, None)
    # dest_state = State(1080, 1085, None)
    # max_steering_radius = 20 # pixels
    # dest_reached_radius = 50 # pixels

    rrt = FastRRTPlanner(world)

    max_num_steps = 100000     # max number of iterations
    max_steering_radius = 150 # pixels
    dest_reached_radius = 150 # pixels
    (plan, cost, num_nodes) = rrt.plan(start_state,
                                dest_state,
                                max_num_steps,
                                max_steering_radius,
                                dest_reached_radius, test=False,
                                filename="fast_rrt_result.png")


