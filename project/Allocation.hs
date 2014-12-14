module Allocation where

import Data.List (union, intersect, (\\), nub)
import AbstractSyntax
import Machine

data Tree a =
    Branch a [Tree a]
  | Finish a
  deriving (Eq, Show)

foldTree :: ([a] -> a) -> Tree a -> a
foldTree f (Branch x ts) = f [x, f [foldTree f t | t <- ts]]
foldTree f (Finish x) = x

-- foldTree sum (Branch 1 [Branch 2 [Finish 3],Branch 4 [Finish 5]])
-- (sum [1, sum [2, 3], sum [4, 5]])

-- smallest :: Ord a => Tree a -> a
-- smallest t = ??? -- Complete for Problem #3, part (b).
--
-- largest :: Ord a => Tree a -> a
-- largest t = ??? -- Complete for Problem #3, part (b).

data Allocation =
    Alloc [(Var, Register)]
  deriving (Eq, Show)


-- Add instance declaration for Problem #3, part (c) here.


-- allocations :: (Interference, [Register]) -> Allocation -> [Var] -> Tree Allocation
-- allocations (conflicts, rs) (Alloc a) (x:xs) = ??? -- Complete for Problem #3, part (d).

-- Useful helper function.
unconflicted ::(Interference, [Register]) -> Allocation -> Var -> [Register]
unconflicted (conflicts, rs) (Alloc a) x = rs \\ [r | (y,r) <- a, (x,y) `elem` conflicts || (y,x) `elem` conflicts]

--eof
