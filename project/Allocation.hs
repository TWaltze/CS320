module Allocation where

import Data.List (union, intersect, (\\), nub)
import AbstractSyntax
import Machine

data Tree a =
    Branch a [Tree a]
  | Finish a
  deriving (Eq, Show)

foldTree :: ([a] -> a) -> Tree a -> a
foldTree f (Branch x ts) = f [f [foldTree f t | t <- ts]]
foldTree f (Finish x) = x

-- foldTree sum (Branch 1 [Branch 2 [Finish 3], Branch 4 [Finish 5]])
-- (sum [1, sum [2, sum [3]], sum [4, sum [5]]])

smallest :: Ord a => Tree a -> a
smallest (Branch x ts) = minimum [foldTree minimum t | t <- ts]
smallest (Finish x) = x

-- (Branch [("d",5)] [Finish [("a",1), ("b",1)], Finish [("x",3), ("y",2)]])
-- f [ [("d",5)], f [ [("a",1), ("b",1)], [("x",3), ("y",2)] ] ]

largest :: Ord a => Tree a -> a
largest (Branch x ts) = maximum [foldTree maximum t | t <- ts]
largest (Finish x) = x

data Allocation =
    Alloc [(Var, Register)]
  deriving (Eq, Show)

-- Add instance declaration for Problem #3, part (c) here.
instance Ord Allocation where
    Alloc a <= Alloc b = length (nub [y | (x, y) <- a]) <= length (nub [y | (x, y) <- b])


-- allocations :: (Interference, [Register]) -> Allocation -> [Var] -> Tree Allocation
allocations (conflicts, rs) (Alloc a) (x:[]) = Finish (Alloc (a ++ [(x, rs!!0)]))
allocations (conflicts, rs) (Alloc a) (x:xs) =
    Branch
    (Alloc a)
    ( [allocations (conflicts, (rs \\ [r])) (Alloc (a ++ [(x, r)])) xs | r <- rs] )

-- Useful helper function.
unconflicted ::(Interference, [Register]) -> Allocation -> Var -> [Register]
unconflicted (conflicts, rs) (Alloc a) x = rs \\ [r | (y,r) <- a, (x,y) `elem` conflicts || (y,x) `elem` conflicts]



--eof
