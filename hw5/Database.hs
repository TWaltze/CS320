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

badExample = [
        Add (User "Bob"),
        Create (Table "Revenue"),
        Insert (Table "Revenue", [("Day", 1), ("Amount", 2400)]),
        Insert (Table "Revenue", [("Day", 2), ("Amount", 1700)]),
        Insert (Table "Revenue", [("Day", 3), ("Amount", 3100)]),
        Allow (User "Alice", Table "Revenue")
    ]

badExample' = [
        Add (User "Alice"),
        Add (User "Bob"),
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
isAllowed commands user table = length [u | Allow (u, t) <- commands, u == user, t == table] > 0

select :: [Command] -> User -> Table -> Column -> Maybe [Integer]
select commands user table column =
    if isAllowed commands user table == True then
        Just [lookup' column d | Insert (t, d) <- commands, table == t]
    else
        Nothing



-- Type synonym for aggregation operators.
type Operator = Integer -> Integer -> Integer

-- Complete for Assignment 5, Problem 1, part (b).
fromJust :: Maybe a -> a
fromJust (Just x) = x

aggregate :: [Command] -> User -> Table -> Column -> Operator -> Maybe Integer
aggregate commands user table column operator =
    if isAllowed commands user table == True then
        Just (foldr operator 0 (fromJust (select commands user table column)))
    else
        Nothing



-- Complete for Assignment 5, Problem 1, part (c).
valid (Allow (user, table)) commands =
    length [u | Add (u) <-commands, u == user] > 0 &&
    length [t | Create (t) <-commands, t == table] > 0
valid (Insert (table, _)) commands =
    length [t | Create (t) <-commands, t == table] > 0
valid _ commands = True

validate :: [Command] -> Bool
validate commands =
    length [command | command <- reverse commands, valid command commands == False] == 0



--eof
