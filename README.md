# seven-wonders

https://j-brooke.github.io/FracturedJson/ 
for json formatting 

run `python3 -m unittest discover -p *Test.py -s test/` to execute tests

run `ruff format` to auto format 
run `ruff check` to run linting


## todo
Handle duplicate player names: `handle duplicate player names`

## done
Wonders B side completed
Support Wonders with multiple effects at a stage [EphesosB, RhodosB, HalikarnassosB]
- free_build (build without resource requirements once per age)
- discard_build (build from the collective discard pool, no cost)  
```Clarification: this special ability takes place at the end of the turn in which this stage is built. If players discard cards this turn (as in the case of the 6th turn of an age), the player can also choose from among them.```  
Guilds
