-- Object Toolkit 50 | 30 Color pulsing light
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local part = script.Parent
assert(part:IsA("BasePart"), "Put this Script inside a BasePart")
local TweenService = game:GetService("TweenService")
local function tween(target, seconds, properties)
    local t = TweenService:Create(target, TweenInfo.new(seconds, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut), properties)
    t:Play()
    t.Completed:Wait()
end
local light = part:FindFirstChildWhichIsA("Light")
assert(light, "Add a Light inside the part")
while part.Parent and light.Parent do
    tween(light, 2, {Color = Color3.fromRGB(80, 150, 255)})
    if not light.Parent then break end
    tween(light, 2, {Color = Color3.fromRGB(210, 90, 255)})
end
