from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "cadical_wrapper.h":

    cdef cppclass CadSolver:
        CadSolver(string)
        CadSolver()
        void add(int)
        void addList(vector[vector[int]] &)
        int solve()
        vector[vector[int]] getProof()
        vector[int] getResults(int)
        double getTime()

cdef class CSolver:
    cdef CadSolver *thisptr
    def __cinit__(self,proof=None):
        if proof:
            self.thisptr = new CadSolver(proof.encode())
        else:
            self.thisptr = new CadSolver()
    def __dealloc__(self):
        del self.thisptr
    def add(self,val):
        self.thisptr.add(val)
    def addList(self,vals):
        self.thisptr.addList(vals)
    def solve(self):
        return self.thisptr.solve()
    def getProof(self):
        return self.thisptr.getProof()
    def getResults(self,max_var):
        return self.thisptr.getResults(max_var)
    def getTime(self):
        return self.thisptr.getTime()

