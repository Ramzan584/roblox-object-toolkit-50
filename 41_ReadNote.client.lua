-- Object Toolkit 50 | 41 Readable note
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local Players = game:GetService("Players")
local player = Players.LocalPlayer
local part = workspace:WaitForChild("NotePart", 15)
assert(part and part:IsA("BasePart"), "Create Workspace.NotePart")
local gui = Instance.new("ScreenGui")
gui.Name = "ToolkitNote"; gui.ResetOnSpawn = false; gui.Parent = player:WaitForChild("PlayerGui")
local panel = Instance.new("TextButton")
panel.Size = UDim2.fromScale(0.65, 0.5); panel.Position = UDim2.fromScale(0.175, 0.25)
panel.BackgroundColor3 = Color3.fromRGB(25, 28, 35); panel.TextColor3 = Color3.fromRGB(245, 245, 245)
panel.TextWrapped = true; panel.TextSize = 22; panel.Visible = false; panel.Parent = gui
local p = Instance.new("ProximityPrompt")
p.ActionText = "Read / Читать"; p.MaxActivationDistance = 10; p.Parent = part
p.Triggered:Connect(function(who)
    if who ~= player then return end
    panel.Text = tostring(part:GetAttribute("NoteText") or "Write NoteText on NotePart") .. "\n\n[Tap to close / Нажми, чтобы закрыть]"
    panel.Visible = true
end)
panel.Activated:Connect(function() panel.Visible = false end)
local connection = game:GetService("RunService").Heartbeat:Connect(function()
    local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
    if not root or not part.Parent or (root.Position - part.Position).Magnitude > 16 then panel.Visible = false end
end)
script.Destroying:Connect(function() connection:Disconnect(); p:Destroy(); gui:Destroy() end)
