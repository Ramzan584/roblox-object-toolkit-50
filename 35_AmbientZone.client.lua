-- Object Toolkit 50 | 35 Client ambient zone
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local player = game:GetService("Players").LocalPlayer
local SoundService = game:GetService("SoundService")
local zone = workspace:WaitForChild("AmbientZone", 15)
assert(zone and zone:IsA("BasePart"), "Create Workspace.AmbientZone Part")
local template = zone:FindFirstChildOfClass("Sound")
assert(template and template.SoundId ~= "", "AmbientZone needs a Sound asset")
local sound = template:Clone()
sound.Name = "ToolkitAmbientLocal"; sound.Looped = true; sound.Parent = SoundService
while script.Parent and zone.Parent do
    local character = player.Character
    local root = character and character:FindFirstChild("HumanoidRootPart")
    local inside = false
    if root then
        local p = zone.CFrame:PointToObjectSpace(root.Position)
        local half = zone.Size / 2
        inside = math.abs(p.X) <= half.X and math.abs(p.Y) <= half.Y and math.abs(p.Z) <= half.Z
    end
    if inside and not sound.IsPlaying then sound:Play() end
    if not inside and sound.IsPlaying then sound:Stop() end
    task.wait(0.2)
end
sound:Destroy()
