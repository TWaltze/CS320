module Allocation where

import Data.List (union, intersect, (\\), nub)
import AbstractSyntax
import Machine

data Tree a =
    Branch a [Tree a]
  | Finish a
  deriving (Eq, Show)

foldTree :: ([a] -> a) -> Tree a -> a
foldTree _ _ = ??? -- Complete for Problem #3, part (a).

smallest :: Ord a => Tree a -> a
smallest t = ??? -- Complete for Problem #3, part (b).

largest :: Ord a => Tree a -> a
largest t = ??? -- Complete for Problem #3, part (b).

data Allocation =
    Alloc [(Var, Register)]
  deriving (Eq, Show)


-- Add instance declaration for Problem #3, part (c) here.


allocations :: (Interference, [Register]) -> Allocation -> [Var] -> Tree Allocation
allocations (conflicts, rs) (Alloc a) (x:xs) = ??? -- Complete for Problem #3, part (d).

-- Useful helper function.
unconflicted ::(Interference, [Register]) -> Allocation -> Var -> [Register]
unconflicted (conflicts, rs) (Alloc a) x = rs \\ [r | (y,r) <- a, (x,y) `elem` conflicts || (y,x) `elem` conflicts]

--eof