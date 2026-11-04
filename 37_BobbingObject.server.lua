-- Object Toolkit 50 | 37 Bobbing decoration
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local part = script.Parent
assert(part:IsA("BasePart"), "Put this Script inside a BasePart")
local RunService = game:GetService("RunService")
local AMPLITUDE, PERIOD = 1.5, 3
part.Anchored = true
local start, elapsed = part.CFrame, 0
local connection = RunService.Heartbeat:Connect(function(dt)
    elapsed = (elapsed + dt) % PERIOD
    part.CFrame = start + Vector3.new(0, math.sin(elapsed / PERIOD * math.pi * 2) * AMPLITUDE, 0)
end)
part.Destroying:Connect(function() connection:Disconnect() end)
