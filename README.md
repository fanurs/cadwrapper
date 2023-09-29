## PREPARING

PYTHON:

Install Cython in your virtual environment:
```bash
pip install cython
```

C++/CADICAL:

The local directory includes a compiled version of `libcadical.a`, but if you need to compile your own, it requires the addiction of Position Indipendent Code. To do this, when compiling your own cadical library, do the following.

```bash
./configure CXXFLAGS="-fPIC"
make
```

The resulting make should have a build directory with `libcadical.a` which you should copy to this python directory.


## INSTALLING

It should install with a single command:
```bash
python setup.py install
```
This will put the module `cadsolver` in your virtual environment.


## USAGE

The module is called `cadsolver` so that is the name you should import.

All work is done by the `CSolver` class. The only argument required is the location/name of the proof file.

```python
mySolver = cadsolver.CSolver("proofs/out.proof")
```

If you do not give a proof file, it will not provide a proof, but will still solve.
Adding the data to solve is done with the addList method, which takes a list of lists. They do NOT need to be null-terminated.

```python
mySolver.addList([[1,-2],[2,-3],[-1,3]])
```

You may also add literals one at a time and null terminate them. For the above list, you could do the following:

```python
mySolver.add(1)
mySolver.add(-2)
mySolver.add(0)
mySolver.add(2)
mySolver.add(-3)
mySolver.add(0)
mySolver.add(-1)
mySolver.add(3)
mySolver.add(0)
```

The 'solve' method returns 10 or 20, if it is Satisfiable or Unsatisfiable

```python
mySolver.solve()
```

If the solve returned 10, you may get the results with getResults(<max variable>)

```python
mySolver.getResults(2)
# [-1,2]

mySolver.getResults(3)
# [-1,2,3]
```

If you need the proof, you can call getProof(). This will both write the proof file, and return a list of lists. The lists will be empty if it is satisfiable.

```python
mySolver.getProof()
# <... file output stuff here>
# [[-1,3],[2],[1],[]]
```

Note that the proofs will end on an empty list due to proofs ending on 0.

You can retrieve the time taken to solve the set with getTime()

```python
mySolver.getTime()
# 0.332
```

If you have not run a solver yet, it will not return a value.
