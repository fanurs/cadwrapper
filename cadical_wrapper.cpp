#include <cadical.hpp>
#include <cadical_wrapper.h>
#include <fstream>
#include <iostream>
#include <chrono>

using namespace std;
using namespace std::chrono;

class ClauseArray : public CaDiCaL::ClauseIterator {
    vector<vector<int> >& res;
public:
    ClauseArray (vector<vector<int> >& inV) : res (inV) { }
  bool clause (const vector<int> & c) {
      vector<int> tv;
    for (const auto & lit : c) {
	tv.push_back(lit);
    }
    res.push_back(tv);
    return true;
  }
};

CadSolver::CadSolver(const string& proof) :
    _proof(proof),
    _solve(0),
    _solveTime(0)
{
    set_long_option ("--no-binary");
    trace_proof(proof.c_str());
}

CadSolver::CadSolver() :
    _proof(""),
    _solve(0),
    _solveTime(0)
{
    set_long_option ("--no-binary");
}


CadSolver::~CadSolver()
{
}

void CadSolver::addList(const vector<vector<int> >& inV)
{
    for (auto it = inV.begin();it!=inV.end();++it)
    {
	for (auto jt = it->begin();jt != it->end();++jt)
	{
	    add(*jt);
	}
	add(0);
    }
    return;
}

vector<vector<int> > CadSolver::getProof()
{
    vector<vector<int> > pV;

    if (_solve != 20 || _proof.empty())
    {
	return pV;
    }
    flush_proof_trace ();
    close_proof_trace ();

    ifstream pfile;
    pfile.open(_proof);
    if (pfile.is_open())
    {
	string nl;
	while (getline(pfile,nl))
	{
	    size_t curr;
	    size_t next = -1;
	    vector<int> ln;
	    do
	    {
		curr = next+1;
		next = nl.find_first_of(' ',curr);
		int r = stoi(nl.substr(curr,next - curr));
		if (r) ln.push_back(r);
	    }
	    while (next != string::npos);
	    pV.push_back(ln);
	}
    }
    
    return pV;
}

int CadSolver::solve()
{
    steady_clock::time_point i1 = steady_clock::now();
    _solve = Solver::solve();
    duration<double> ts = duration_cast<duration<double> >(steady_clock::now() - i1);
    _solveTime = (ts.count());
    return _solve;
}

vector<int> CadSolver::getResults(int max_var)
{    
    vector<int> res;
    if (_solve != 10)
    {
	return res;
    }
    for (int i = 1;i <= max_var;++i)
    {
	res.push_back(val(i) < 0 ? -i : i);
    }
    return res;
}
