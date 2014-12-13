module Interpret where

import AbstractSyntax
import Parse
import TypeCheck

eval :: [(String, Bool)] -> Exp -> Bool
eval _ _ = False -- Implement for Problem #1, part (b).

exec :: [(String, Bool)] -> Stmt -> ([(String, Bool)], Output)
exec env (Print    e s) =
  let (env', o) = exec env s
  in (env', [eval env e] ++ o)
exec env _ = (env, []) -- Implement the Assign and End cases for Problem #1, part (b).

interpret :: Stmt -> Maybe Output
interpret _ = Nothing -- Implement for Problem #1, part (d).

-- eof