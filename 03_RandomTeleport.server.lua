-- Object Toolkit 50 | 03 Random destination teleport
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
local folder = reference(part, "Destinations", "Folder")
local random = Random.new()
local cooldown = setmetatable({}, {__mode = "k"})
onUse(prompt(part, "Random teleport"), part, function(player)
    if (cooldown[player] or 0) > os.clock() then return end
    local choices = {}
    for _, candidate in ipairs(folder:GetChildren()) do
        if candidate:IsA("BasePart") and candidate:IsDescendantOf(workspace) then table.insert(choices, candidate) end
    end
    if #choices == 0 then return end
    local character, _, root = actor(player, part, 12)
    if not character then return end
    local target = choices[random:NextInteger(1, #choices)]
    cooldown[player] = os.clock() + 2
    character:PivotTo(target.CFrame + Vector3.new(0, target.Size.Y / 2 + 4, 0))
    root.AssemblyLinearVelocity = Vector3.zero
    root.AssemblyAngularVelocity = Vector3.zero
end)
