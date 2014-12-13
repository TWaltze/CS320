module Interpret where

import AbstractSyntax
import Parse
import TypeCheck

eval :: [(String, Bool)] -> Exp -> Bool
eval env (Value v) = v
eval env (Not e) = not (eval env e)
eval env (And e1 e2) = (eval env e1) && (eval env e2)
eval env (Or e1 e2) = (eval env e1) || (eval env e2)
eval env (Variable x) = lookup' x env

exec :: [(String, Bool)] -> Stmt -> ([(String, Bool)], Output)
exec env (Print    e s) =
  let (env', o) = exec env s
  in (env', [eval env e] ++ o)
exec env (Assign x e s) =
    let v = eval env e
        env' = env ++ [(x, v)]
        (env'', o) = exec env' s
    in (env'', o)
exec env _ = (env, [])

interpret :: Stmt -> Maybe Output
interpret s =
    if fromJust (chk [] s) == Void then
        let (env, o) = exec [] s
        in Just o
    else Nothing

-- eof
