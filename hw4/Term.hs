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
evaluate _ = 0 -- Modify and complete for Problem 4.

--eof