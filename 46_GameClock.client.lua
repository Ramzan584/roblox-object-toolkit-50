-- Object Toolkit 50 | 46 Game clock HUD
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local player = Players.LocalPlayer
local gui = Instance.new("ScreenGui")
gui.Name = "ToolkitClock"; gui.ResetOnSpawn = false
local old = player:WaitForChild("PlayerGui"):FindFirstChild(gui.Name)
if old then old:Destroy() end
gui.Parent = player:WaitForChild("PlayerGui")
local label = Instance.new("TextLabel")
label.Position = UDim2.new(0, 16, 0, 16)
label.Size = UDim2.fromOffset(260, 34)
label.BackgroundColor3 = Color3.fromRGB(22, 25, 33)
label.BackgroundTransparency = 0.15
label.TextColor3 = Color3.fromRGB(235, 240, 255)
label.TextSize = 18; label.Parent = gui

local Lighting = game:GetService("Lighting")
local connection = RunService.Heartbeat:Connect(function()
    local minutes = math.floor(Lighting.ClockTime * 60) % 1440
    label.Text = string.format("%02d:%02d", math.floor(minutes / 60), minutes % 60)
end)
script.Destroying:Connect(function() connection:Disconnect(); gui:Destroy() end)
