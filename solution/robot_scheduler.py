import csv
from collections import deque
from abc import ABC, abstractmethod


class Robot(ABC):
    """
    An abstract base class for a robot.

    Attributes:
        - robot_id (int): The ID of the robot.
        - robot_type (str): The type of the robot.
        - velocity (int): The number of seconds it takes the robot to move from one node to another.
        - state (int): The state of the robot. 1 represents working, 2 represents waiting, and 3 represents moving.
        - path (deque): A deque representing the path that the robot will follow.
        - time_left (int): The number of seconds left for the robot in its current state.
        - time_spend (int): The overall time that the robot has spent.
    """

    def __init__(self, robot_id: int, robot_type: str, velocity: int, state: int, path: deque, time_left: int, time_spend: int):
        self.robot_id = robot_id
        self.robot_type = robot_type
        self.velocity = velocity
        self.state = state
        self.path = path
        self.time_left = time_left
        self.time_spend = time_spend

    @abstractmethod
    def action(self, node_type: str) -> int:
        '''
        Abstract method that needs to be implemented by subclasses. 
        Returns an integer based on the node type.
        '''
        pass


class Organizer(Robot):
    """
    A subclass of Robot representing an organizer robot.

    Attributes:
        Inherits all attributes from Robot.

    Methods:
        - action(node_type: str) -> int: 
            Takes in a node_type parameter and returns the time it takes for the robot to complete its action at that node.
    """

    def __init__(self, robot_id: int, robot_type: str, velocity: int, state: int, path: deque, time_left: int, time_spend: int):
        super().__init__(robot_id, robot_type, velocity, state, path, time_left, time_spend)

    def action(self, node_type: str) -> int:
        if node_type == 'A':
            return 30
        elif node_type == 'B':
            return 45
        else:
            raise ValueError(
                f"Invalid node_type '{node_type}'. Must be 'A' or 'B'.")


class Mover(Robot):
    """
    A subclass of Robot representing an mover robot.

    Attributes:
        Inherits all attributes from Robot.

    Methods:
        - action(node_type: str) -> int: 
            Takes in a node_type parameter and returns the time it takes for the robot to complete its action at that node.
    """

    def __init__(self, robot_id: int, robot_type: str, velocity: int, state: int, path: deque, time_left: int, time_spend: int):
        super().__init__(robot_id, robot_type, velocity, state, path, time_left, time_spend)

    def action(self, node_type: str) -> int:
        if node_type == 'A':
            return 20
        elif node_type == 'B':
            return 35
        else:
            raise ValueError(
                f"Invalid node_type '{node_type}'. Must be 'A' or 'B'.")


class Platform:
    """
    A class to represent a platform in the factory.

    Attributes:
        platform_id (int): The unique ID of the platform.
        node_type (str): The type of the node connected to the platform (either 'A' or 'B').
        state (int): The current state of the platform (1: busy, 2: free).
        time_left (int): The number of seconds left for the platform to finish all tasks at the current time.
        cur_visitor (deque): A queue of robots that are currently at this platform.
        visitor (list): A list of all robots that have come to this platform.
    """

    def __init__(self, platform_id: int, node_type: str, state: int, time_left: int, cur_visitor: deque, visitor: list) -> None:
        self.platform_id = platform_id
        self.node_type = node_type
        self.state = state
        self.time_left = time_left
        self.cur_visitor = cur_visitor
        self.visitor = visitor


class RobotScheduler:
    """
    A class representing a scheduler for a group of robots and platforms.

    Attributes:
        robots (list): A list of Robot objects.
        platform_map (dict): A dictionary mapping from platform_id to Platform objects.
        times (int): The number of time steps taken by the scheduler.

    Methods:
        - __init__(robots: list, platform_map: dict): 
            Initializes the scheduler with the given robots and platform_map, setting the initial state, time_left, and cur_visitor for each robot and platform objects.
        - run(): 
            Runs the scheduler, updating the state of the robots and platforms at each time step until all robots have completed their paths.
    """

    def __init__(self, robots: list, platform_map: dict):
        # Initialize the robots, platforms, and times.
        self.robots = [robots[i] for i in [0, 2, 1, 3]]
        self.platform_map = platform_map
        self.times = 0

        # Initialize the state, time_left, and cur_visitor for each robot and platform.
        for robot in self.robots:
            platform = self.platform_map[robot.path[0]]

            robot.state = 1 # Set robot state to working
            robot.time_left = robot.action(platform.node_type)

            platform.state = 1 # Set platform state to busy
            platform.time_left = robot.action(platform.node_type)
            platform.cur_visitor.append(robot.robot_id) # Add the corresponding robot to cur_visitor
            platform.visitor.append(robot.robot_id)

    def run(self):
        # Initialize flag to True.
        flag = True

        while flag:
            # Set flag to False.
            flag = False
            # Increment the times.
            self.times += 1

            for robot in sorted(self.robots, key = lambda r : r.state): # First consider the robot at work
                if not robot.path:  # If robot has completed its path, move on to next robot.
                    continue
                else:
                    # At least one robot is still working.
                    flag = True

                # Increment the time_spend of the robot.
                robot.time_spend += 1

                # If the robot still has time left on its current task, keep the current state
                if robot.time_left > 0:
                    if robot.state == 1:  # Robot is working.
                        platform = self.platform_map[robot.path[0]]
                        robot.time_left -= 1
                        platform.time_left -= 1
                    elif robot.state == 2:  # Robot is waiting.
                        robot.time_left -= 1
                    elif robot.state == 3:  # Robot is moving.
                        robot.time_left -= 1
                else:
                    # If the robot has completed its current task, change the current state
                    if robot.state == 1:  # Robot was working.
                        platform = self.platform_map[robot.path[0]]
                        robot.state = 3  # Set robot state to moving.
                        robot.time_left = robot.velocity - 1
                        robot.path.popleft()
                        platform.cur_visitor.popleft()
                        if platform.cur_visitor:
                            platform.time_left -= 1
                        else:
                            platform.state = 2  # Set platform state to free.
                            platform.time_left = 0
                    elif robot.state == 2:  # Robot was waiting.
                        platform = self.platform_map[robot.path[0]]
                        robot.state = 1  # Set robot state to working.
                        robot.time_left = robot.action(platform.node_type) - 1
                    elif robot.state == 3:  # Robot was moving.
                        platform = self.platform_map[robot.path[0]]
                        platform.cur_visitor.append(robot.robot_id)
                        if not platform.visitor or platform.visitor[-1] != robot.robot_id:
                            platform.visitor.append(robot.robot_id)
                        if platform.state == 1:  # Platform is busy.
                            robot.state = 2  # Set robot state to waiting.
                            robot.time_left = platform.time_left
                            platform.time_left += robot.action(platform.node_type)
                        elif platform.state == 2:  # Platform is free.
                            robot.state = 1  # Set robot state to working.
                            platform.state = 1  # Set platform state to busy.
                            robot.time_left = robot.action(platform.node_type) - 1
                            platform.time_left = robot.action(platform.node_type) - 1


class InputReader:
    """
    A class that reads input files and returns corresponding objects for robots and platforms.

    Methods:
        - read_robots(robots_file_path: str, paths_file_path: str) -> Tuple[List[Robot], Dict[int, Robot]]:
            Takes in the file paths for robots and paths and returns a list of Robot objects and a dictionary mapping robot IDs to Robot objects.
        - read_platforms(nodes_file_path: str) -> Tuple[List[Platform], Dict[int, Platform]]:
            Takes in the file path for nodes and returns a list of Platform objects and a dictionary mapping platform IDs to Platform objects.
    """

    def read_robots(self, robots_file_path, paths_file_path):
        robots = []
        robot_map = {}

        with open(robots_file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                robot_id = int(row[0])
                robot_type = row[1]
                velocity = int(row[2])
                state = 1
                path = deque([])
                time_left = 0
                time_spend = 0
                if robot_type == 'organizer':
                    robot = Organizer(robot_id, robot_type, velocity, state, path, time_left, time_spend)
                elif robot_type == 'mover':
                    robot = Mover(robot_id, robot_type, velocity, state, path, time_left, time_spend)
                else:
                    raise ValueError(f'Invalid robot type: {robot_type}')
                robot_map[robot_id] = robot
                robots.append(robot)

        with open(paths_file_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                robot_id = int(row[0])
                postion = int(row[1])
                for robot in robots:
                    if robot.robot_id == robot_id:
                        robot.path.append(postion)
                        break

        return robots, robot_map

    def read_platforms(self, nodes_file_path):
        platforms = []
        platform_map = {}

        with open(nodes_file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                platform_id = int(row[0])
                node_type = row[1]
                state = 2
                time_left = 0
                cur_visitor = deque([])
                visitor = []
                platform = Platform(platform_id, node_type, state, time_left, cur_visitor, visitor)
                platform_map[platform_id] = platform
                platforms.append(platform)

        return platforms, platform_map


class OutputWriter:
    """
    This class represents a module for writing the output files.

    Attributes:
        robots: a list of Robot objects representing all robots in the simulation.
        platforms: a list of Platform objects representing all platforms in the simulation.

    Methods:
        - write_robot_info(file_path: str) -> None:
            Writes the robot ID and total time spent to a CSV file specified by the file_path parameter.
        - write_platform_info(file_path: str) -> None:
            Writes the platform ID and visitor information to a CSV file specified by the file_path parameter.
    """

    def __init__(self, robots, platforms):
        self.robots = robots
        self.platforms = platforms

    def write_robot_info(self, file_path):
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Robot ID', 'Total Time'])
            for robot in self.robots:
                writer.writerow([robot.robot_id, robot.time_spend])

    def write_platform_info(self, file_path):
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Platform ID', 'Visitor 1', 'Visitor 2', 'Visitor 3', 'Visitor 4'])
            for platform in self.platforms:
                row = [platform.platform_id] + platform.visitor
                writer.writerow(row)


if __name__ == '__main__':
    # Read input data
    reader = InputReader()
    robots, robot_map = reader.read_robots('../input_data/robots_input.csv', '../input_data/paths_input.csv')
    platforms, platform_map = reader.read_platforms('../input_data/nodes_input.csv')

    # Schedule robots
    scheduler = RobotScheduler(robots, platform_map)
    scheduler.run()

    # Write output data
    writer = OutputWriter(robots, platforms)
    writer.write_robot_info('../output_data/robot_info.csv')
    writer.write_platform_info('../output_data/platform_info.csv')

    # Print total time for each robot
    for robot in robots:
        print(f'Robot {robot.robot_id} total time: {robot.time_spend}')
