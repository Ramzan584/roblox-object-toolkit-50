-- Object Toolkit 50 | 16 Conveyor belt
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local part = script.Parent
assert(part:IsA("BasePart"), "Put this Script inside a BasePart")
local SPEED = 14
local DIRECTION = part.CFrame.LookVector
part.Anchored = true
part.AssemblyLinearVelocity = DIRECTION * SPEED
