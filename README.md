# sequence-diagram
A tool for creating simple ASCII sequence diagrams. 
This is a local implementation, so you don't risk leaking IP as in online UML solutions.

## example:
input:
```
alice to bob: apple pie
bob: smiles
bob to alice: blueberry pie
alice: smiles
alice to charlie: strawberry pie
charlie to bob: money
bob to alice: paycheck
alice: contemplates life, the universe, and everything
alice to charlie: a complex poem of intricate concepts
bob to charlie: a giant hotdog-shaped car and two chocolate bars
charlie: nirvana
```

output:
```
alice               bob                 charlie             

apple pie---------->

                    [smiles]

 <------------------blueberry pie

[smiles]

strawberry pie------------------------->

                     <------------------money

 <------------------paycheck

[contemplates life,
the universe, and
everything]

a complex poem of
intricate concepts
          ----------------------------->

                    a giant hotdog-
                    shaped car and two
                    chocolate bars----->

                                        [nirvana]

```

## getting started
- `git clone https://github.com/dansgithubuser/sequence-diagram`
- `python -m sequence-diagram sequence-diagram/example.txt`
