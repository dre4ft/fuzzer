roadmap :
- ajouter les autres types  : mut, etc 
- ajouter l4iunterface graphiaue aka la WebUI *P1*
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
