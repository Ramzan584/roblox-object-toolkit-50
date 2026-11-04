-- Object Toolkit 50 | 39 Camera distance fade
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local RunService = game:GetService("RunService")
local target = workspace:WaitForChild("FadeObject", 15)
assert(target and target:IsA("BasePart"), "Create Workspace.FadeObject Part")
local old = target.LocalTransparencyModifier
local connection = RunService.RenderStepped:Connect(function()
    local camera = workspace.CurrentCamera
    if camera and target.Parent then
        local distance = (camera.CFrame.Position - target.Position).Magnitude
        target.LocalTransparencyModifier = math.clamp(1 - distance / 12, 0, 1)
    end
end)
script.Destroying:Connect(function()
    connection:Disconnect()
    if target.Parent then target.LocalTransparencyModifier = old end
end)
