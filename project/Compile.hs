module Compile where

import AbstractSyntax
import Allocation
import Machine

class Compilable a where
    comp :: [(Var, Register)] -> a -> Instruction

instance Compilable Stmt where
    comp xrs (End) = STOP (Register 0)
    -- comp xrs (Print e s) = STOP (Register -1)
    -- comp xrs (Assign x e s) = STOP (Register -1)

instance Compilable Exp where
    comp xrs (Variable x) = STOP (lookup' x xrs)
    -- comp xrs (Value b) =
    --     let next = (topOfStack xrs) + 1
    --     in if b == False then
    --         INIT (next) ()
    --     else
    --         INIT (next) (FLIP next ())
    comp xrs (Not e) = comp xrs e


topOfStack :: [(Var, Register)] -> Register
topOfStack xrs = maximum [r | (x, r) <- xrs]

-- result :: Instruction -> Register
-- result (STOP r) = r
-- result (INIT _ i) = result i
-- result (FLIP _ i) = result i
-- result (COPY _ _ i) = result i
-- result (NAND _ _ _ i) = result i


-- compileMin :: Stmt -> Maybe Instruction
-- compileMin _ = STOP (Register -1) -- Complete for Problem #4, part (c).

compileMax :: Integer -> Stmt -> Maybe Instruction
compileMax _ _ = Nothing -- Complete for Problem #4, part (d).

-- eof
