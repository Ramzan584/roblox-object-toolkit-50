-- Object Toolkit 50 | 05 Teleport to another place
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
local PLACE_ID = 0 -- Set your destination PlaceId, not an experience/universe ID.
local TeleportService = game:GetService("TeleportService")
if PLACE_ID <= 0 then warn("PlaceTeleport: configure PLACE_ID first"); return end
local p = prompt(part, "Travel / Перейти")
local pending = setmetatable({}, {__mode = "k"})
TeleportService.TeleportInitFailed:Connect(function(player)
    pending[player] = nil
end)
onUse(p, part, function(player)
    if pending[player] then return end
    local ticket = {}
    pending[player] = ticket
    local ok, err = pcall(function() TeleportService:TeleportAsync(PLACE_ID, {player}) end)
    if not ok then pending[player] = nil; warn("Teleport failed: " .. tostring(err)) end
    task.delay(15, function() if pending[player] == ticket then pending[player] = nil end end)
end)
