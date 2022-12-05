#include <cadical.hpp>
#include <vector>
#include <string>

class CadSolver: public CaDiCaL::Solver
{
public:
    CadSolver(const std::string& proof);
    CadSolver();
    virtual ~CadSolver();

    void addList(const std::vector<std::vector<int> >& inV);
    std::vector<std::vector<int> > getProof();
    std::vector<int> getResults(int max_var);
    int solve();
    double getTime() { return _solveTime;}

private:
    std::string _proof;
    int _solve;
    double _solveTime;
};
