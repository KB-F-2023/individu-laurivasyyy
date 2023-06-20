from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

V = TypeVar('V') # variable type
D = TypeVar('D') # domain type

class Constraint(Generic[V, D], ABC):
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...

class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables # variables to be constrained
        self.domains: Dict[V, List[D]] = domains # domain of each variable
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        if len(assignment) == len(self.variables):
            return assignment

        unassigned: List[V] = [v for v in self.variables if v not in assignment]

        first: V = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            # if we're still consistent, we recurse (continue)
            if self.consistent(first, local_assignment):
                result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None


class MapColoringConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2

    def satisfied(self, assignment: Dict[str, str]) -> bool: 
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        return assignment[self.place1] != assignment[self.place2]

if __name__ == "__main__": 
    variables: List[str] = ["Western Australia", "Northern Territory", "South Australia",
    "Queensland", "New South Wales", "Victoria", "Tasmania"]

    domains: Dict[str, List[str]] = {}
    for variable in variables: 
        domains = {v: ["sienna", "tan", "wheat"] for v in variables}

    csp: CSP[str, str] = CSP(variables, domains)
    csp.add_constraint(MapColoringConstraint("Western Australia", "Northern Territory"))
    csp.add_constraint(MapColoringConstraint("Western Australia", "South Australia"))
    csp.add_constraint(MapColoringConstraint("South Australia", "Northern Territory"))
    csp.add_constraint(MapColoringConstraint("Queensland", "Northern Territory"))
    csp.add_constraint(MapColoringConstraint("Queensland", "South Australia"))
    csp.add_constraint(MapColoringConstraint("Queensland", "New South Wales"))
    csp.add_constraint(MapColoringConstraint("New South Wales", "South Australia"))
    csp.add_constraint(MapColoringConstraint("Victoria", "South Australia"))
    csp.add_constraint(MapColoringConstraint("Victoria", "New South Wales"))
    csp.add_constraint(MapColoringConstraint("Victoria", "Tasmania"))
    
    # Solve the problem
solution: Optional[Dict[str, str]] = csp.backtracking_search()
if solution is None:
    print("No solution found!")
else:
    print(solution)

    # Define the map coordinates
    map_coordinates = {
        "Western Australia": ((110, 0), (129, 0), (129, -35), (112, -35)),
        "Northern Territory": ((129, 0), (138, 0), (138, -26), (129, -26)),
        "South Australia": ((129, -26), (141, -26), (141, -35), (129, -35)),
        "Queensland": ((138, 0), (154, 0), (154, -29), (138, -29)),
        "New South Wales": ((141, -26), (154, -26), (154, -35), (141, -35)),
        "Victoria": ((141, -35), (149, -35), (149, -39), (141, -39)),
        "Tasmania": ((144, -39), (149, -39), (149, -44), (144, -44))
    }

    # Define the colors
    colors = {
        "sienna": "#A0522D",
        "tan": "#D2B48C",
        "wheat": "#F5DEB3"
    }

    # Create the figure and axis objects
    fig, ax = plt.subplots()

    # Plot each state
    for state, coords in map_coordinates.items():
        poly = Polygon(coords, facecolor=colors[solution[state]])
        ax.add_patch(poly)

    # Set the x and y limits
    ax.set_xlim([110, 154])
    ax.set_ylim([-44, 0])

    # Show the plot
    plt.show()