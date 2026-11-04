-- Object Toolkit 50 | 50 Camera viewpoint toggle
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local Players = game:GetService("Players")
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")
local player = Players.LocalPlayer
local point = workspace:WaitForChild("CameraPoint", 15)
assert(point and point:IsA("BasePart"), "Create Workspace.CameraPoint Part")
local active, saved = false, nil
local function restore()
    if not saved then return end
    local camera = saved.camera
    if camera and camera == workspace.CurrentCamera then
        camera.CameraType = saved.kind
        camera.CameraSubject = saved.subject
        camera.CFrame = saved.frame
    end
    saved = nil; active = false
end
local inputConnection = UserInputService.InputBegan:Connect(function(input, processed)
    if processed or UserInputService:GetFocusedTextBox() or input.KeyCode ~= Enum.KeyCode.C then return end
    if active then restore(); return end
    local camera = workspace.CurrentCamera
    if not camera or not point.Parent then return end
    saved = {camera = camera, kind = camera.CameraType, subject = camera.CameraSubject, frame = camera.CFrame}
    active = true
    camera.CameraType = Enum.CameraType.Scriptable
    camera.CFrame = point.CFrame
end)
local frameConnection = RunService.RenderStepped:Connect(function()
    if not active then return end
    if not point.Parent or workspace.CurrentCamera ~= saved.camera then restore(); return end
    saved.camera.CFrame = point.CFrame
end)
local characterConnection = player.CharacterAdded:Connect(restore)
script.Destroying:Connect(function()
    restore(); inputConnection:Disconnect(); frameConnection:Disconnect(); characterConnection:Disconnect()
end)
