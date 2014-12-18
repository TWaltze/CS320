module Compile where

import AbstractSyntax
import Allocation
import Machine

class Compilable a where
    comp :: [(Var, Register)] -> a -> Instruction

instance Compilable Stmt where
    comp xrs (End) = STOP (Register 0)
    comp xrs (Print e s) =
        let expression = comp xrs e
        in  expression +++
            (COPY (Register 0) (result expression)
            (comp xrs s))
    comp xrs (Assign x e s) =
        let expression = comp xrs e
        in  expression +++
            (comp ((x, (result expression)):xrs) s)

instance Compilable Exp where
    comp xrs (Variable x) = STOP (lookup' x xrs)
    comp xrs (Value b) =
        let next = (topOfStack xrs) + 1
        in if b == False then
            INIT (next)
            (STOP next)
        else
            INIT (next)
            (FLIP next
            (STOP next))
    comp xrs (Not e) =
        let expression = comp xrs e
        in  expression +++
            (FLIP (result expression)
            (STOP (result expression)))
    comp xrs (And e1 e2) =
        let expression1 = comp xrs e1
            expression2 = comp xrs e2
            r1 = result expression1
            r2 = result expression2
        in  expression1 +++
            expression2 +++
            (NAND r1 r2 (r2 + 1)
            (FLIP (r2 + 1)
            (STOP (r2 + 1))))
    -- comp xrs (Or e1 e2) =
    --     let expression1 = comp xrs e1
    --         expression2 = comp xrs e2
    --         r1 = result expression1
    --         r2 = result expression2
    --     in  expression1 +++
    --         expression2 +++
    --         (NAND r1 r2 (r2 + 1)
    --         (FLIP (r2 + 1)
    --         (STOP (r2 + 1))))


topOfStack :: [(Var, Register)] -> Register
topOfStack xrs = maximum [r | (x, r) <- xrs]

result :: Instruction -> Register
result (STOP r) = r
result (INIT _ i) = result i
result (FLIP _ i) = result i
result (COPY _ _ i) = result i
result (NAND _ _ _ i) = result i


-- compileMin :: Stmt -> Maybe Instruction
-- compileMin _ = STOP (Register -1) -- Complete for Problem #4, part (c).

compileMax :: Integer -> Stmt -> Maybe Instruction
compileMax _ _ = Nothing -- Complete for Problem #4, part (d).

-- eof
