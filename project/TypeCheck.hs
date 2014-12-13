module TypeCheck where

import AbstractSyntax
import Parse

class Typeable a where
  chk :: [(String, Type)] -> a -> Maybe Type
  
instance Typeable Exp where 
  chk _ _ = Nothing -- Implement for Problem #1, part (c).

instance Typeable Stmt where 
  chk _ _ = Nothing -- Implement for Problem #1, part (c).

-- eof