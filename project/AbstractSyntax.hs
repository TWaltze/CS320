module AbstractSyntax where

import Data.List (union, intersect, (\\), nub)

type Var = String
type Output = [Bool]

data Stmt =
    Print Exp Stmt
  | Assign Var Exp Stmt
  | End
  deriving (Eq, Show)

data Exp =
    Variable Var
  | Value Bool
  | And Exp Exp
  | Or Exp Exp
  | Not Exp
  deriving (Eq, Show)

data Type =
    Bool
  | Void
  deriving (Eq, Show)

-- Useful helper functions.
lookup' :: Eq a => a -> [(a, b)] -> b
lookup' x ((x',i) : rest) = if x == x' then i else lookup' x rest

addOrReplace :: Eq a => a -> b -> [(a, b)] -> [(a, b)]
addOrReplace key value assoc = (key, value):(filter ((key /=).fst) assoc)

-- Type class for a polymorphic fold function on abstract syntax trees.
--
--  * The first argument is the aggregator for combining
--    results of recursive folds.
--  * The second argument is a function that will be applied to
--    (i.e., and will replace) Variable nodes.
--  * The third argument is a constant that will replace all
--    non-Variable leaf nodes (i.e., Value nodes).
--  * The fourth argument is the abstract syntax tree that
--    will be folded.

class Foldable b where
  fold :: ([a] -> a) -> (String -> a) -> a -> b -> a

instance Foldable Exp where
  fold f var b (Variable x ) = var x
  fold f var b (Value v    ) = b
  fold f var b (And   e1 e2) = f [fold f var b e1, fold f var b e2]
  fold f var b (Or    e1 e2) = f [fold f var b e1, fold f var b e2]
  fold f var b (Not   e    ) = f [fold f var b e]

instance Foldable Stmt where
  fold f var b (Print e s) = f [fold f var b e, fold f var b s]
  fold f var b (Assign x e s) = f [fold f var b e, fold f var b s]
  fold f var b (End) = b



class HasVariables a where
  vars :: a -> [Var]

instance HasVariables Stmt where
  vars s = nub (fold (concat) (\x -> [x]) [] s)

instance HasVariables Exp where
  vars e = nub (fold (concat) (\x -> [x]) [] e)



unbound :: Stmt -> [Var]
unbound (Print e s) = (vars e) `union` (unbound s)
unbound (Assign x e s) = (vars e) `union` ((unbound s) \\ [x])
unbound (End) = []

-- Print (Variable "x") (Assign "a" (Value True) (Print (Variable "a") End))
{--
[x] `union` [] = [x]
Print (Variable "x") => [x]
    [x]
Assign "a" (Value True) (Print (Variable "a") End) => [] `union` ([a] \\ [a]) = []
    (Value True) => []
        []
    (Print (Variable "a") End) => [a] `union` [] = [a]
        (Variable "a")
            [a]
        End
            []
--}

type Interference = [(Var, Var)]

interference :: Stmt -> Interference
interference (Print e s) = interference s
interference (Assign x e s) = interference s ++ ([(x, y) | y <- (vars e) `union` (unbound s), y /= x])
interference (End) = []

-- eof
