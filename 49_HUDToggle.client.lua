-- Object Toolkit 50 | 49 HUD toggle key
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local UserInputService = game:GetService("UserInputService")
local player = game:GetService("Players").LocalPlayer
local playerGui = player:WaitForChild("PlayerGui")
local TARGETS = {"ToolkitClock", "ToolkitCompass", "ToolkitCoordinates"}
local hidden, saved = false, {}
local function apply(gui)
    if not gui:IsA("ScreenGui") or not table.find(TARGETS, gui.Name) then return end
    if hidden then
        if saved[gui] == nil then saved[gui] = gui.Enabled end
        gui.Enabled = false
    end
end
local childConnection = playerGui.ChildAdded:Connect(apply)
local connection = UserInputService.InputBegan:Connect(function(input, processed)
    if processed or UserInputService:GetFocusedTextBox() or input.KeyCode ~= Enum.KeyCode.H then return end
    hidden = not hidden
    if hidden then for _, gui in ipairs(playerGui:GetChildren()) do apply(gui) end
    else
        for gui, enabled in pairs(saved) do if gui.Parent then gui.Enabled = enabled end end
        saved = {}
    end
end)
script.Destroying:Connect(function()
    connection:Disconnect(); childConnection:Disconnect()
    for gui, enabled in pairs(saved) do if gui.Parent then gui.Enabled = enabled end end
end)
