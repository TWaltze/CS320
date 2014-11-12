---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 4 (skeleton code)
-- Tree.hs
--

data Tree =
    Leaf
  | Twig
  | Branch Tree Tree Tree
  deriving (Eq, Show)

twigs(Leaf) = 0
twigs(Twig) = 1
twigs(Branch x y z) = twigs(x) + twigs(y) + twigs(z)

branches(Leaf) = 0
branches(Twig) = 0
branches(Branch x y z) = 1 + branches(x) + branches(y) + branches(z)

height(Leaf) = 0
height(Twig) = 1
height(Branch x y z) = 1 + maximum[height(x), height(y), height(z)]

perfect(Leaf) = False
perfect(Twig) = False
perfect(Branch Leaf Leaf Leaf) = True
perfect(Branch x y z) = perfect(x) && perfect(y) && perfect(z) && x == y && x == z

-- degenerate(Leaf) = True
-- degenerate(Twig) = True
-- degenerate(Branch x y z) = (degenerate(x) && degenerate(y)) || (degenerate(x) && degenerate(z)) || (degenerate(y) && degenerate(z))

degenerate(Leaf) = True
degenerate(Twig) = True
degenerate(Branch Leaf Leaf x) = True && degenerate(x)
degenerate(Branch Leaf Twig x) = True && degenerate(x)
degenerate(Branch Twig Twig x) = True && degenerate(x)
degenerate(Branch Twig Leaf x) = True && degenerate(x)
degenerate(Branch Leaf x Leaf) = True && degenerate(x)
degenerate(Branch Leaf x Twig) = True && degenerate(x)
degenerate(Branch Twig x Twig) = True && degenerate(x)
degenerate(Branch Twig x Leaf) = True && degenerate(x)
degenerate(Branch x Leaf Leaf) = True && degenerate(x)
degenerate(Branch x Leaf Twig) = True && degenerate(x)
degenerate(Branch x Twig Twig) = True && degenerate(x)
degenerate(Branch x Twig Leaf) = True && degenerate(x)
degenerate(_) = False

-- infinite(n) = [n] ++ infinite(n + 1)
infinite = Branch infinite infinite infinite






--eof
