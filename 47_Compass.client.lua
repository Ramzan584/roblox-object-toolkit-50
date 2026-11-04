-- Object Toolkit 50 | 47 Compass HUD
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local player = Players.LocalPlayer
local gui = Instance.new("ScreenGui")
gui.Name = "ToolkitCompass"; gui.ResetOnSpawn = false
local old = player:WaitForChild("PlayerGui"):FindFirstChild(gui.Name)
if old then old:Destroy() end
gui.Parent = player:WaitForChild("PlayerGui")
local label = Instance.new("TextLabel")
label.Position = UDim2.new(0, 16, 0, 56)
label.Size = UDim2.fromOffset(260, 34)
label.BackgroundColor3 = Color3.fromRGB(22, 25, 33)
label.BackgroundTransparency = 0.15
label.TextColor3 = Color3.fromRGB(235, 240, 255)
label.TextSize = 18; label.Parent = gui

local connection = RunService.RenderStepped:Connect(function()
    local camera = workspace.CurrentCamera
    if not camera then return end
    local look = camera.CFrame.LookVector
    local heading = math.deg(math.atan2(look.X, -look.Z)) % 360
    local names = {"N", "NE", "E", "SE", "S", "SW", "W", "NW"}
    label.Text = string.format("%s  %03d°", names[math.floor((heading + 22.5) / 45) % 8 + 1], math.floor(heading))
end)
script.Destroying:Connect(function() connection:Disconnect(); gui:Destroy() end)
