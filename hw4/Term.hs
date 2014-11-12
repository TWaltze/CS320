---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 4 (skeleton code)
-- Term.hs
--

data Term =
    Number Integer
  | Abs Term
  | Plus Term Term
  | Mult Term Term

evaluate :: Term -> Integer
evaluate(Number x) = x
evaluate(Plus x y) = evaluate(x) + evaluate(y)
evaluate(Mult x y) = evaluate(x) * evaluate(y)
evaluate(Abs x) = abs(evaluate(x))

--eof
