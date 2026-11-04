-- Object Toolkit 50 | 10 Two button gate
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local Players = game:GetService("Players")
local function actor(player, origin, range)
    local character = player and player.Character
    local humanoid = character and character:FindFirstChildOfClass("Humanoid")
    local root = character and character:FindFirstChild("HumanoidRootPart")
    if not humanoid or humanoid.Health <= 0 or not root then return end
    if origin and (root.Position - origin.Position).Magnitude > range then return end
    return character, humanoid, root
end
local function touchedPlayer(hit, origin)
    local model = hit:FindFirstAncestorOfClass("Model")
    local player = model and Players:GetPlayerFromCharacter(model)
    if player and actor(player, origin, origin.Size.Magnitude / 2 + 8) then return player end
end
local function reference(parent, name, class)
    local value = parent:FindFirstChild(name)
    local target = value and value:IsA("ObjectValue") and value.Value
    assert(target and target:IsA(class), "Add ObjectValue '" .. name .. "' pointing to " .. class)
    return target
end
local function prompt(parent, action)
    local p = Instance.new("ProximityPrompt")
    p.Name = "ToolkitPrompt"
    p.ActionText = action
    p.ObjectText = parent.Name
    p.MaxActivationDistance = 10
    p.HoldDuration = 0.15
    p.Parent = parent
    return p
end
local function onUse(p, origin, callback)
    p.Triggered:Connect(function(player)
        if p.Enabled and actor(player, origin, p.MaxActivationDistance + 2) then callback(player) end
    end)
end
local part = script.Parent
assert(part:IsA("BasePart"), "Put this Script inside a BasePart")
local TweenService = game:GetService("TweenService")
local function tween(target, seconds, properties)
    local t = TweenService:Create(target, TweenInfo.new(seconds, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut), properties)
    t:Play()
    t.Completed:Wait()
end
local a = reference(part, "ButtonA", "BasePart")
local b = reference(part, "ButtonB", "BasePart")
assert(a ~= b, "ButtonA and ButtonB must be different")
part.Anchored = true
local pressed, busy, closed = {}, false, part.CFrame
local function press(button)
    if busy then return end
    pressed[button] = os.clock()
    if not pressed[a] or not pressed[b] or math.abs(pressed[a] - pressed[b]) > 5 then return end
    busy = true; pressed = {}
    tween(part, 1, {CFrame = closed + Vector3.new(0, part.Size.Y + 1, 0)})
    task.wait(4)
    if part.Parent then tween(part, 1, {CFrame = closed}) end
    busy = false
end
onUse(prompt(a, "Button A"), a, function() press(a) end)
onUse(prompt(b, "Button B"), b, function() press(b) end)
