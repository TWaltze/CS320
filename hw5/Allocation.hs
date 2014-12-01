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

instance Ord Alloc where
    Alloc x y < Alloc a b = abs(x - y) < abs(a - b)
    Alloc x y <= Alloc a b = abs(x - y) <= abs(a - b)

instance Ord Graph where
     x < y = alloc x < alloc y
     x <= y = alloc x <= alloc y



graph :: Alloc -> [Item] -> Graph
graph (Alloc x y) items =
    if null (tail items) == False then
        Branch (Alloc x y) ( graph (Alloc (x + head items) y) (tail items) ) ( graph (Alloc x (y + head items)) (tail items) )
    else
        Branch (Alloc x y) (Finish (Alloc (x + head items) y)) (Finish (Alloc x (y + head items)))


alloc :: Graph -> Alloc
alloc (Branch (Alloc x y) _ _) = Alloc x y
alloc (Finish (Alloc x y)) = Alloc x y


final :: Graph -> [Alloc]
final (Branch _ x y) = [] ++ final x ++ final y
final (Finish (Alloc x y)) = [Alloc x y]


depth :: Integer -> Graph -> [Alloc]
depth level (Branch (Alloc x y) left right) =
    if level == 0 then
        [Alloc x y]
    else
        (depth (level - 1) left) ++ (depth (level - 1) right)
depth level (Finish (Alloc x y)) =
    if level == 0 then
        [Alloc x y]
    else
        []


greedy :: Strategy
greedy (Branch _ left right) = min left right

-- allocTree :: Graph -> Alloc -> Graph
-- allocTree (Branch a left right) target =
--     if a == target then
--         (Branch a left right)
--     else if alloc (allocTree left target) == target then
--         left
--     else
--         right
-- allocTree (Finish (Alloc x y)) target = (Finish (Alloc x y))


graphsAtDepth :: Integer -> Graph -> [Graph]
graphsAtDepth level (Branch (Alloc x y) left right) =
    if level == 0 then
        [(Branch (Alloc x y) left right)]
    else
        (graphsAtDepth (level - 1) left) ++ (graphsAtDepth (level - 1) right)
graphsAtDepth level (Finish (Alloc x y)) =
    if level == 0 then
        [(Finish (Alloc x y))]
    else
        []


patient :: Integer -> Strategy
patient level (Branch (Alloc x y) left right) = minimum (graphsAtDepth level (Branch (Alloc x y) left right))


optimal :: Strategy
optimal graph = Finish (minimum (final graph))

--eof
