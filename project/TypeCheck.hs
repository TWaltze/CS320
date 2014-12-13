module TypeCheck where

import AbstractSyntax
import Parse

fromJust :: Maybe a -> a
fromJust (Just x) = x

class Typeable a where
  chk :: [(String, Type)] -> a -> Maybe Type

instance Typeable Exp where
    chk env (Value _) = Just Bool
    chk env (And e1 e2) =
        if fromJust (chk env e1) == Bool && fromJust (chk env e2) == Bool then
            Just Bool
        else Nothing
    chk env (Or e1 e2) =
        if fromJust (chk env e1) == Bool && fromJust (chk env e2) == Bool then
            Just Bool
        else Nothing
    chk env (Not e) =
        if fromJust (chk env e) == Bool then
            Just Bool
        else Nothing
    chk env (Variable x) = Just (lookup' x env)

instance Typeable Stmt where
    chk env (End) = Just Void
    chk env (Print e s) =
        if fromJust (chk env e) == Bool && fromJust (chk env s) == Void then
            Just Void
        else Nothing
    chk env (Assign x e s) =
        let env' = env ++ [(x, fromJust (chk env e))]
        in chk env' s

-- eof
