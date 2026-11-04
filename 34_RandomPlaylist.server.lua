-- Object Toolkit 50 | 34 Random playlist
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local part = script.Parent
assert(part:IsA("BasePart"), "Put this Script inside a BasePart")
local random = Random.new()
local previous
while part.Parent do
    local choices = {}
    for _, sound in ipairs(part:GetChildren()) do
        if sound:IsA("Sound") and sound.SoundId ~= "" then table.insert(choices, sound) end
    end
    if #choices == 0 then warn("RandomPlaylist: add permitted Sound assets"); return end
    local selected = choices[random:NextInteger(1, #choices)]
    if #choices > 1 and selected == previous then
        for _, sound in ipairs(choices) do if sound ~= previous then selected = sound; break end end
    end
    for _, sound in ipairs(choices) do sound:Stop() end
    selected.Looped = false
    selected:Play()
    local elapsed = 0
    repeat task.wait(0.25); elapsed = elapsed + 0.25
    until not part.Parent or not selected.Parent or not selected.IsPlaying or elapsed >= 180
    if selected.Parent then selected:Stop() end
    previous = selected
    task.wait(0.5)
end
