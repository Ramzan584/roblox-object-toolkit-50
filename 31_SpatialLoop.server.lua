-- Object Toolkit 50 | 31 Spatial looping sound
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local part = script.Parent
assert(part:IsA("BasePart"), "Put this Script inside a BasePart")
local sound = part:FindFirstChildOfClass("Sound")
assert(sound and sound.SoundId ~= "", "Add Sound with a permitted SoundId")
sound.Looped = true
sound.RollOffMinDistance = 5; sound.RollOffMaxDistance = 60
sound:Play()
