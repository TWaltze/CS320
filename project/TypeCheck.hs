module TypeCheck where

import AbstractSyntax
import Parse

fromJust :: Maybe a -> a
fromJust (Just x) = x

isJust         :: Maybe a -> Bool
isJust Nothing = False
isJust _       = True

class Typeable a where
  chk :: [(String, Type)] -> a -> Maybe Type

instance Typeable Exp where
    chk env (Value _) = Just Bool
    chk env (And e1 e2) =
        if isJust (chk env e1) && isJust (chk env e2) && fromJust (chk env e1) == Bool && fromJust (chk env e2) == Bool then
            Just Bool
        else Nothing
    chk env (Or e1 e2) =
        if isJust (chk env e1) && isJust (chk env e2) && fromJust (chk env e1) == Bool && fromJust (chk env e2) == Bool then
            Just Bool
        else Nothing
    chk env (Not e) =
        if isJust (chk env e) && fromJust (chk env e) == Bool then
            Just Bool
        else Nothing
    chk env (Variable x) =
        if length [v | (y, v) <- env, x == y]  > 0 then
            Just (lookup' x env)
        else Nothing

instance Typeable Stmt where
    chk env (End) = Just Void
    chk env (Print e s) =
        if isJust (chk env e) && isJust (chk env s) && fromJust (chk env e) == Bool && fromJust (chk env s) == Void then
            Just Void
        else Nothing
    chk env (Assign x e s) =
        let added = chk env e
        in if isJust added then
                let env' = env ++ [(x, fromJust (chk env e))]
                in chk env' s
            else Nothing

-- eof
