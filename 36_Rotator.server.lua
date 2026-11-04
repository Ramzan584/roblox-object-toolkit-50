-- Object Toolkit 50 | 36 Rotating decoration
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local part = script.Parent
assert(part:IsA("BasePart"), "Put this Script inside a BasePart")
local RunService = game:GetService("RunService")
local SPEED = math.rad(45)
part.Anchored = true
local start, angle = part.CFrame, 0
local connection = RunService.Heartbeat:Connect(function(dt)
    angle = (angle + SPEED * dt) % (math.pi * 2)
    part.CFrame = start * CFrame.Angles(0, angle, 0)
end)
part.Destroying:Connect(function() connection:Disconnect() end)
