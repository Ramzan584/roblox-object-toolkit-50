-- Object Toolkit 50 | 20 Physical servo shuttle
-- MIT | timura032 | Setup: README / INSTALL_RU_EN.txt
local part = script.Parent
assert(part:IsA("BasePart"), "Put this Script inside a BasePart")
local TRAVEL, SPEED = 20, 6
local guide = Instance.new("Part")
guide.Name = part.Name .. "_Guide"
guide.Size = Vector3.new(1, 1, 1)
guide.CFrame = part.CFrame
guide.Anchored = true; guide.Transparency = 1
guide.CanCollide = false; guide.CanTouch = false; guide.CanQuery = false
guide.Parent = part.Parent
local a = Instance.new("Attachment"); a.Parent = guide
local b = Instance.new("Attachment"); b.Parent = part
local servo = Instance.new("PrismaticConstraint")
servo.Attachment0 = a; servo.Attachment1 = b
servo.LimitsEnabled = true; servo.LowerLimit = 0; servo.UpperLimit = TRAVEL
servo.ActuatorType = Enum.ActuatorType.Servo
servo.Speed = SPEED; servo.ServoMaxForce = 1000000; servo.LinearResponsiveness = 35
servo.Parent = guide
part.Anchored = false
part:SetNetworkOwner(nil)
local far = true
while part.Parent and guide.Parent do
    servo.TargetPosition = far and TRAVEL or 0
    far = not far
    task.wait(TRAVEL / SPEED + 2)
end
if guide.Parent then guide:Destroy() end
if b.Parent then b:Destroy() end
