class CSP:
    def __init__(self, variables, domains, sum_neighbors, constraints, n, expected_sum, board):
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.sum_neighbors = sum_neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0
        self.n_bt = 0
        self.n = n 
        self.expected_sum = expected_sum
        self.board = board
    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]
    def nconflicts(self, var, val, assignment):
        count = 0
        i = int(var)//self.n
        j = int(var)% self.n
        if (i >= 2):
            var2 = str((i-1)*self.n + j)
            var3 = str((i-2)*self.n + j)
            val2 = None
            val3 = None
            if assignment.__contains__(var2):
                val2 = assignment[var2]
            if assignment.__contains__(var3):
                val2 = assignment[var3] 
            if val2 is not None and val3 is not None and self.constraints(var, val, var2, val2, var3 , val3) is False:
                count += 1
        if (j >= 2):
            var2 = str((i)*self.n + j -1 )
            var3 = str((i)*self.n + j - 1)
            val2 = None
            val3 = None
            if assignment.__contains__(var2):
                val2 = assignment[var2]
            if assignment.__contains__(var3):
                val2 = assignment[var3] 
            if val2 is not None and val3 is not None and self.constraints(var, val, var2, val2, var3 , val3) is False:
                count += 1
        if (i <= self.n - 3):
            var2 = str((i+1)*self.n + j)
            var3 = str((i+2)*self.n + j)
            val2 = None
            val3 = None
            if assignment.__contains__(var2):
                val2 = assignment[var2]
            if assignment.__contains__(var3):
                val2 = assignment[var3] 
            if val2 is not None and val3 is not None and self.constraints(var, val, var2, val2, var3 , val3) is False:
                count += 1
        if (j <= self.n - 3):
            var2 = str((i)*self.n + j + 1)
            var3 = str((i)*self.n + j + 2)
            val2 = None
            val3 = None
            if assignment.__contains__(var2):
                val2 = assignment[var2]
            if assignment.__contains__(var3):
                val2 = assignment[var3] 
            if val2 is not None and val3 is not None and self.constraints(var, val, var2, val2, var3 , val3) is False:
                count += 1            
        sum_row = 0
        for k in range(0, self.n):
            var2 = str((i)*self.n + k)
            if assignment.__contains__(var2):
                val2 = assignment[var2]
                sum_row += int(val2) 

        if sum_row + self.sum_neighbors.get(var)[0] > self.expected_sum:
            count += 1

        sum_column = 0
        for k in range(0, self.n):
            var2 = str((k)*self.n + j)
            if assignment.__contains__(var2):
                val2 = assignment[var2]
                sum_column += int(val2) 

        if sum_column + self.sum_neighbors.get(var)[1] > self.expected_sum:
            count += 1


        return count 

    def display(self, assignment):
        print('CSP:', self, 'with assignment:', assignment)

    def goal_test(self, state):
        assignment = dict(state)
        test_ =  (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))
        strs_ = []
        print(self.board)
        for i in range(self.n):
            row = []
            str_ = ""
            for j in range(self.n):
                var = str(i*self.n + j)
                if self.board[i][j] == '-':
                    self.board[i][j] = assignment[var]
                str_ += self.board[i][j]
            strs_.append(str_)
        print(board)
        for j in range(self.n):
            str_ = ""
            for i in range(self.n):
                str_ += board[i][j]
            strs_.append(str_)
        if len(strs_) != len(list(set(strs_))):
            test_ = False
        return test_


    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        return (self.curr_domains or self.domains)[var]

    def restore(self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)


def AC3(csp, queue=None, removals=None):
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]
    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xi:
                    queue.append((Xk, Xi))
    return True


def revise(csp, Xi, Xj, removals):
    revised = False
    for x in csp.curr_domains[Xi][:]:
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised

def first_unassigned_variable(assignment, csp):
    for var in csp.variables:
        if var not in assignment:
            return var

def mrv(assignment, csp):
    vars_to_check = []
    size = []
    for v in csp.variables:
        if v not in assignment.keys():
            vars_to_check.append(v)
            size.append(num_legal_values(csp, v, assignment))
    return vars_to_check[size.index(min(size))]

def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        count = 0
        for val in csp.domains[var]:
            if csp.nconflicts(var, val, assignment) == 0:
                count += 1
        return count


def unordered_domain_values(var, assignment, csp):
    return csp.choices(var)


def lcv(var, assignment, csp):
    return sorted(csp.choices(var),
                  key=lambda val: csp.nconflicts(var, val, assignment))


# Inference


def no_inference(csp, var, value, assignment, removals):
    return True


def forward_checking(csp, var, value, assignment, removals):
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
    return True


def mac(csp, var, value, assignment, removals):
    return AC3(csp, [(X, var) for X in csp.neighbors[var]], removals)

def backtracking_search(csp,
                        select_unassigned_variable,
                        order_domain_values,
                        inference):
    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                    else:
                        csp.n_bt += 1
                csp.restore(removals)

        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result


def different_values_constraint(A, a, B, b, C, c):
    if a != b:
        return True
    elif a == b:
        return c != a

class BinaryPuzzle(CSP):

    def __init__(self, board, n, expected_sum):
        self.domains = {}
        self.board = board
        self.n = n 
        self.sum_neighbors = {}
        self.expected_sum = expected_sum
        variables = []
        for i in range(n):
            for j in range(n):
                var = str(i*n +j)
                if self.board[i][j] != '-':
                    self.domains.update({var: str(self.board[i][j])})
                else:
                    self.domains.update({var: '01'})
                self.check_two_row(i,j)
                self.check_two_column(i,j)
        for i in range(n):
            for j in range(n):
                var = str(i*n +j)
                if len(self.domains[var]) > 1:
                    variables.append(var)

        for i in range(n):
            for j in range(n):
                var = str(i*n +j)
                self.sum_neighbors.update({var: [self.sum_row(i), self.sum_column(j)]})

        #print(self.domains, self.sum_neighbors, different_values_constraint, self.n, self.expected_sum)

        CSP.__init__(self, variables, self.domains, self.sum_neighbors, different_values_constraint, self.n, self.expected_sum, self.board)

    def check_two_row(self, i , j):
        var = str(i*self.n +j)
        if  j >= 2:
            if self.board[i][j-1] == self.board[i][j-2] and self.board[i][j-2] == '0':
                self.domains.update({var: '1'})
            elif self.board[i][j-1] == self.board[i][j-2] and self.board[i][j-2] == '1':
                self.domains.update({var: '0'})
        if  j <= self.n - 3:
            if self.board[i][j+1] == self.board[i][j+2] and self.board[i][j+2] == '0':
                self.domains.update({var: '1'})
            elif self.board[i][j+1] == self.board[i][j+2] and self.board[i][j+2] == '1':
                self.domains.update({var: '0'})
        return

    def check_two_column(self, i, j):
        var = str(i*self.n +j)
        if  i >= 2:
            if self.board[i-1][j] == self.board[i-2][j] and self.board[i-2][j] == '0':
                self.domains.update({var: '1'})
            if self.board[i-1][j] == self.board[i-2][j] and self.board[i-2][j] == '1':
                self.domains.update({var: '0'}) 
        if  i <= self.n -3:
            if self.board[i+1][j] == self.board[i+2][j] and self.board[i+2][j] == '0':
                self.domains.update({var: '1'})
            if self.board[i+1][j] == self.board[i+2][j] and self.board[i+2][j] == '1':
                self.domains.update({var: '0'})   
        return 

    def sum_row (self, i ):
        sum_ = 0
        for j in range(0, self.n):
            if self.board[i][j] != '-':
                sum_ += int(self.board[i][j])
        return sum_

    def sum_column (self, j):
        sum_ = 0
        for i in range(0, self.n):
            if self.board[i][j] != '-':
                sum_ += int(self.board[i][j])
        return sum_
    