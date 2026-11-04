-- Object Toolkit 50 | 27 Flickering light
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local part = script.Parent
assert(part:IsA("BasePart"), "Put this Script inside a BasePart")
local light = part:FindFirstChildWhichIsA("Light")
assert(light, "Add a Light inside the part")
local initial = light.Enabled
local random = Random.new()
while part.Parent and light.Parent do
    light.Enabled = random:NextNumber() > 0.25
    task.wait(random:NextNumber(0.08, 0.5))
end
if light.Parent then light.Enabled = initial end
