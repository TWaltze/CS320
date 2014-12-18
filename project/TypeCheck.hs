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
        let v1 = chk env e1
            v2 = chk env e2
        in if isJust (v1) && isJust (v2) && fromJust (v1) == Bool && fromJust (v2) == Bool then
            Just Bool
        else Nothing
    chk env (Or e1 e2) =
        let v1 = chk env e1

            v2 = chk env e2
        in if isJust (v1) && isJust (v2) && fromJust (v1) == Bool && fromJust (v2) == Bool then
            Just Bool
        else Nothing
    chk env (Not e) =
        let v = chk env e
        in if isJust (v) && fromJust (v) == Bool then
            Just Bool
        else Nothing
    chk env (Variable x) =
        if length [v | (y, v) <- env, x == y]  > 0 then
            Just (lookup' x env)
        else Nothing

instance Typeable Stmt where
    chk env (End) = Just Void
    chk env (Print e s) =
        let v1 = chk env e
            v2 = chk env s
        in if isJust (v1) && isJust (v2) && fromJust (v1) == Bool && fromJust (v2) == Void then
            Just Void
        else Nothing
    chk env (Assign x e s) =
        let v1 = chk env e
        in if isJust v1 then
                let env' = env ++ [(x, fromJust (v1))]
                in chk env' s
            else Nothing

-- eof
