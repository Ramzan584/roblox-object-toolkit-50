-- Object Toolkit 50 | 48 Player coordinates HUD
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local player = Players.LocalPlayer
local gui = Instance.new("ScreenGui")
gui.Name = "ToolkitCoordinates"; gui.ResetOnSpawn = false
local old = player:WaitForChild("PlayerGui"):FindFirstChild(gui.Name)
if old then old:Destroy() end
gui.Parent = player:WaitForChild("PlayerGui")
local label = Instance.new("TextLabel")
label.Position = UDim2.new(0, 16, 0, 96)
label.Size = UDim2.fromOffset(260, 34)
label.BackgroundColor3 = Color3.fromRGB(22, 25, 33)
label.BackgroundTransparency = 0.15
label.TextColor3 = Color3.fromRGB(235, 240, 255)
label.TextSize = 18; label.Parent = gui

local elapsed = 0
local connection = RunService.Heartbeat:Connect(function(dt)
    elapsed = elapsed + dt
    if elapsed < 0.1 then return end
    elapsed = 0
    local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
    if root then
        local p = root.Position
        label.Text = string.format("X %.1f   Y %.1f   Z %.1f", p.X, p.Y, p.Z)
    else label.Text = "Waiting for character…" end
end)
script.Destroying:Connect(function() connection:Disconnect(); gui:Destroy() end)
