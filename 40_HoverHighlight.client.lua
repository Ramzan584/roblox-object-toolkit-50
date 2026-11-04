-- Object Toolkit 50 | 40 Mouse hover highlight
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local player = game:GetService("Players").LocalPlayer
local RunService = game:GetService("RunService")
local folder = workspace:WaitForChild("Interactables", 15)
assert(folder and folder:IsA("Folder"), "Create Workspace.Interactables Folder")
local mouse = player:GetMouse()
local highlight = Instance.new("Highlight")
highlight.Name = "ToolkitHover"; highlight.FillTransparency = 0.8
highlight.Parent = workspace
local connection = RunService.RenderStepped:Connect(function()
    local target = mouse.Target
    highlight.Adornee = target and target:IsDescendantOf(folder) and target or nil
end)
script.Destroying:Connect(function() connection:Disconnect(); highlight:Destroy() end)
