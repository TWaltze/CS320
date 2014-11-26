---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 5 (skeleton code)
-- Database.hs
--

module Database where

type Column = String
data User = User String deriving (Eq, Show)
data Table = Table String deriving (Eq, Show)
data Command =
    Add User
  | Create Table
  | Allow (User, Table)
  | Insert (Table, [(Column, Integer)])
  deriving (Eq, Show)

example = [
    Add (User "Alice"),
    Add (User "Bob"),
    Create (Table "Revenue"),
    Insert (Table "Revenue", [("Day", 1), ("Amount", 2400)]),
    Insert (Table "Revenue", [("Day", 2), ("Amount", 1700)]),
    Insert (Table "Revenue", [("Day", 3), ("Amount", 3100)]),
    Allow (User "Alice", Table "Revenue")
  ]

-- Useful function for retrieving a value from a list
-- of (label, value) pairs.
lookup' :: Column -> [(Column, Integer)] -> Integer
lookup' c' ((c,i):cvs) = if c == c' then i else lookup' c' cvs

-- Complete for Assignment 5, Problem 1, part (a).
select :: [Command] -> User -> Table -> Column -> Maybe [Integer]
select _ _ _ _ =
  Nothing



-- Type synonym for aggregation operators.
type Operator = Integer -> Integer -> Integer

-- Complete for Assignment 5, Problem 1, part (b).
aggregate :: [Command] -> User -> Table -> Column -> Operator -> Maybe Integer
aggregate _ _ _ _ _ =
  Nothing



-- Complete for Assignment 5, Problem 1, part (c).
validate :: [Command] -> Bool
validate _ =
  False



--eof