roadmap :
- ajouter les autres types  : mut, etc 
- mqnqgment des wordlists 
- ajouter custom print et verbose
- JWT fuzzer :
    - BF sur des cles venant d4une password list 
    - fuzzing sur les champs ( mutations )
    - wordlist de JWT a tester 
    - test de JWT sans alg


utilisation : 
a date 4 type de fuzzing proposés :

- range : 
    - prend en parametre le debut et la fin du range, ex : range,1-10

- wordlist : 
    - prend en parametre le path dela wordlist, ex: wordlist,password.txt

- regex : 
    - prend en parametre le regex et le nombre d'iteration, ex : regex,^[a-z0-9]{2,10}$,10

- random (alphanumerique)
    - prend en parametre la taille de la chaine et le nombre d'iteration ex : rand,10,10


comment run :

2 options : 

- webUI :

`python3 main.py server [--host] [--port]`

- cli 
`python3 main.py cli fuzztype host [--method] [--headers] [--body]`

les headers et methodes doivent etre en format JSON ex: {"Content-Type":"application/json"}' 

il est important de specifier le content type par defaut c'est du x-www-form-urlencoded
