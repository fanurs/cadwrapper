from __future__ import annotations
import itertools

import numpy as np

import cadsolver

def check_satisfiable(assignments: dict[int, bool], clauses: list[list[int]]) -> bool:
    """Check if given assignments satisfy all clauses.
    
    Parameters
    ----------
    assignments : dict[int, bool]
        Mapping of variables, represented by integer keys, to their boolean
        assignments. Users are responsible to ensure all variables in clauses
        are assigned.
    clauses : list[list[int]]
        Conjunctive normal form (CNF) expression.
        
    Returns
    -------
    satisfiability : bool
        True if the assignments make all clauses True, otherwise False.
    """
    for clause in clauses:
        satisfied = False
        
        # check if at least one literal in clause is satisfied
        for literal in clause:
            variable = abs(literal)
            if (literal > 0) == assignments[variable]:
                satisfied = True
                break
            
        # if this clause is not satisfied,
        # then the whole expression which is AND of all clauses is not satisfied
        if not satisfied:
            return False
    
    # all clauses are satisfied
    return True

def find_satisfiable_brute_force(clauses: list[list[int]], return_all=False) -> dict[int, bool] | list[dict[int, bool]] | None:
    """Find satisfying assignment(s) by brute force.
    
    Parameters
    ----------
    clauses : list[list[int]]
        Conjunctive normal form (CNF) expression. For example, [[1, 2], [-1]]
        represents two clauses, [1, 2] and [-1]. There are two literals (1 and
        2) in the first clause, and one literal (-1) in the second clause. This
        is equivalent to the logical statement (1 or 2) and (-1), where 1 and 2
        can be replaced by boolean variables.
    return_all : bool, default False
        If True, return all satisfying assignments. Otherwise, return the first
        one found.
    
    Returns
    -------
    assignments : dict[int, bool] | list[dict[int, bool]] | None
        Satifying assignment(s) if found, otherwise return None. If `return_all`
        is True, return a list of all satisfying assignments. If `return_all` is
        False, return the first satisfying assignment found.
    """
    # get all variables in the clauses
    variables = set(abs(lit) for clause in clauses for lit in clause)
    if 0 in variables:
        raise ValueError('Literal 0 is prohibited.')
    variables = sorted(variables)

    # brute force loop
    solutions = []
    for assignment in itertools.product([False, True], repeat=len(variables)):
        assignment = {var: boolean for var, boolean in zip(variables, assignment)}
        if check_satisfiable(assignment, clauses):
            solutions.append(assignment)
            if not return_all:
                break # return first satisfying assignment
    
    if len(solutions) == 0 or solutions[0] == dict():
        return None # no satisfying assignment found
    if return_all:
        return solutions
    return solutions[0]

def convert_to_compact_assignment(assignment: dict[int, bool]) -> list[int]:
    result = []
    for variable, boolean in dict(sorted(assignment.items())).items():
        if variable <= 0:
            raise ValueError('Found non-positive variables (keys) in assignment.')
        sign = +1 if boolean else -1
        result.append(sign * variable)
    return result

def convert_to_expanded_assignment(assignment: list[int]) -> dict[int, bool]:
    return {abs(lit): (lit > 0) for lit in assignment}

def build_random_clauses(
    max_n_variables: int,
    max_n_clauses: int,
    max_n_literals_per_clause: int,
    seed=None,
) -> list[list[int]]:
    rand = np.random.RandomState(seed)
    n_variables = rand.randint(1, max_n_variables + 1) # at least one variable
    variables = list(range(1, n_variables + 1))
    n_clauses = rand.randint(0, max_n_clauses + 1) # could have no clauses
    return [
        [
            rand.choice([-1, +1]) * var
            for var in rand.choice(variables, size=rand.randint(1, max_n_literals_per_clause + 1), replace=True)
        ] for _ in range(n_clauses)
    ]

def test_compare_brute_force():
    for _ in range(10_000):
        clauses = build_random_clauses(
            max_n_variables=10,
            max_n_clauses=10,
            max_n_literals_per_clause=10,
        )
        variables = sorted(set(abs(lit) for clause in clauses for lit in clause))

        solver = cadsolver.CSolver()
        solver.addList(clauses)
        solver.solve()
        max_variable = 0 if len(variables) == 0 else variables[-1]
        candidate = solver.getResults(max_variable)

        if candidate: # candidate claims satisfiable
            assignment = convert_to_expanded_assignment(candidate)
            assert check_satisfiable(assignment, clauses)
            continue

        # candidate claims unsatisfiable
        # check with brute force result
        expected = find_satisfiable_brute_force(clauses, return_all=True)
        assert not expected
    
    # TODO
    # - profile time: cadsolver v.s. brute force
    # - ratio of satisfiable and unsatisfiable

