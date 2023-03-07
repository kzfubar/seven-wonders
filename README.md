# seven-wonders

https://j-brooke.github.io/FracturedJson/ 
for json formatting 

run `black . ` from the top level directory to format all files

run `python3 -m unittest discover -p *Test.py -s test/` to execute tests

run `flake8 --ignore=E501,W503,E203` to test lint rules



## todo
Handle duplicate player names: `handle duplicate player names`

Add B side wonders
- Add WondersB.json

Support wonder power effects
- guild_copy (at the end of the age, copy a guild from either neighbor)
- play_last_card (at the end of the age, you may play, discard, bury the last card in your hand, paying any resource costs required)

only play one guild?
could not play caravanasery 
Compare VP at EOG

## done
Support Wonders with multiple effects at a stage [EphesosB, RhodosB, HalikarnassosB]
- free_build (build without resource requirements once per age)
- discard_build (build from the collective discard pool, no cost)  
```Clarification: this special ability takes place at the end of the turn in which this stage is built. If players discard cards this turn (as in the case of the 6th turn of an age), the player can also choose from among them.```  
Guilds