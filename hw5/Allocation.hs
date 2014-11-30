---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 5 (skeleton code)
-- Allocation.hs
--

module Allocation where

type Item = Integer
type Bin = Integer

data Alloc = Alloc Bin Bin deriving (Eq, Show)

data Graph =
    Branch Alloc Graph Graph
  | Finish Alloc
  deriving (Eq, Show)

type Strategy = Graph -> Graph



graph :: Alloc -> [Item] -> Graph
graph (Alloc x y) items =
    if null (tail items) == False then
        Branch (Alloc x y) ( graph (Alloc (x + head items) y) (tail items) ) ( graph (Alloc x (y + head items)) (tail items) )
    else
        Branch (Alloc x y) (Finish (Alloc (x + head items) y)) (Finish (Alloc x (y + head items)))



--eof
