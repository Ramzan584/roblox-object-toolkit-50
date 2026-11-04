-- Object Toolkit 50 | 26 Day night cycle
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local DAY_MINUTES = 12
local Lighting = game:GetService("Lighting")
local RunService = game:GetService("RunService")
local connection = RunService.Heartbeat:Connect(function(dt)
    Lighting.ClockTime = (Lighting.ClockTime + dt * 24 / (DAY_MINUTES * 60)) % 24
end)
script.Destroying:Connect(function() connection:Disconnect() end)
