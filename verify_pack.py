from pathlib import Path
import ctypes,json,ast,xml.etree.ElementTree as ET,hashlib,zipfile,shutil
P=Path(__file__).resolve().parent
items=json.loads((P/'catalogue.json').read_text())
for item in items:item['path']=str(next(P.rglob(item['file'])))
lib=ctypes.CDLL('liblua5.4.so.0');lib.luaL_newstate.restype=ctypes.c_void_p
lib.luaL_openlibs.argtypes=[ctypes.c_void_p]
lib.luaL_loadbufferx.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t,ctypes.c_char_p,ctypes.c_char_p]
lib.lua_pcallk.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_longlong,ctypes.c_void_p]
lib.lua_tolstring.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p];lib.lua_tolstring.restype=ctypes.c_char_p
lib.lua_close.argtypes=[ctypes.c_void_p]
def execute(code,name,run=True):
 s=lib.luaL_newstate();lib.luaL_openlibs(s);b=code.encode();status=lib.luaL_loadbufferx(s,b,len(b),name.encode(),None)
 if not status and run:status=lib.lua_pcallk(s,0,0,0,0,None)
 error=lib.lua_tolstring(s,-1,None).decode() if status else None;lib.lua_close(s)
 if error:raise AssertionError(error)
for item in items:execute(Path(item['path']).read_text(),item['file'],False)
prelude="\nlocal checks, now = 0, 100\nlocal function eq(a,b,name) assert(a==b,name..': expected '..tostring(b)..', got '..tostring(a)); checks=checks+1 end\nlocal function near(a,b,name) assert(math.abs(a-b)<0.000001,name);checks=checks+1 end\nlocal function event()\n local e={callbacks={}}\n function e:Connect(fn) local c={fn=fn,active=true};self.callbacks[#self.callbacks+1]=c;return {Disconnect=function() c.active=false end} end\n function e:Fire(...) for _,c in ipairs(self.callbacks) do if c.active then c.fn(...) end end end\n return e\nend\nlocal tasks={}\nlocal function resumeThread(co,...)\n local ok,wait=coroutine.resume(co,...);assert(ok,wait)\n if coroutine.status(co)~='dead' then tasks[#tasks+1]={at=now+(wait or 0),co=co} end\nend\ntask={}\nfunction task.spawn(fn,...) local co=coroutine.create(fn);resumeThread(co,...);return co end\nfunction task.wait(delay) return coroutine.yield(delay) end\nfunction task.delay(delay,fn) local co=coroutine.create(fn);tasks[#tasks+1]={at=now+delay,co=co} end\nlocal function advance(target)\n local runs=0\n while true do\n  local index,earliest=nil,math.huge\n  for i,t in ipairs(tasks) do if t.at<earliest then index,earliest=i,t.at end end\n  if not index or earliest>target+0.0000001 then break end\n  local t=table.remove(tasks,index);now=earliest;resumeThread(t.co)\n  runs=runs+1;assert(runs<1000,'unbounded scheduler')\n end\n now=target\nend\nEnum=setmetatable({},{__index=function(t,k)local group=setmetatable({},{__index=function(_,v)return k..'.'..v end});rawset(t,k,group);return group end})\nlocal vm={}\nvm.__index=function(v,k)if k=='Magnitude' then return math.sqrt(v.X*v.X+v.Y*v.Y+v.Z*v.Z) end end\nvm.__add=function(a,b)return Vector3.new(a.X+b.X,a.Y+b.Y,a.Z+b.Z) end\nvm.__sub=function(a,b)return Vector3.new(a.X-b.X,a.Y-b.Y,a.Z-b.Z) end\nVector3={new=function(x,y,z)return setmetatable({X=x,Y=y,Z=z},vm) end};Vector3.zero=Vector3.new(0,0,0)\nVector2={new=function(x,y)return {X=x,Y=y} end};UDim2={new=function(...)return {...} end};UDim={new=function(...)return {...} end}\nlocal cm={__add=function(a,b)return CFrame.new(a.Position+b) end}\nCFrame={new=function(v)return setmetatable({Position=v},cm) end}\nColor3={fromRGB=function(...)return {...} end};PhysicalProperties={new=function(...)return {...} end};typeof=type\nlocal methods={}\nlocal objectMeta={__index=function(t,k)return methods[k] or t._props[k] end}\nobjectMeta.__newindex=function(t,k,v)\n if k=='Parent' then\n  local old=t._props.Parent\n  if old then for i,c in ipairs(old._children) do if c==t then table.remove(old._children,i);break end end end\n  t._props.Parent=v\n  if v then\n   v._children[#v._children+1]=t;v.ChildAdded:Fire(t)\n   local a=v\n   while a do a.DescendantAdded:Fire(t);a=a.Parent end\n  end\n else t._props[k]=v end\nend\nInstance={}\nfunction Instance.new(cls)\n local t=setmetatable({_props={ClassName=cls,Name=cls,Value=0,Transparency=0,CanCollide=true,CanTouch=true,Health=100,Color='original',Anchored=true},_children={},_attrs={}},objectMeta)\n for _,key in ipairs({'Touched','PlayerAdded','PlayerRemoving','CharacterAdded','ChildAdded','DescendantAdded','Heartbeat'}) do t._props[key]=event() end\n return t\nend\nfunction methods:IsA(cls)return cls==self.ClassName or (cls=='BasePart' and (self.ClassName=='Part' or self.ClassName=='SpawnLocation')) end\nfunction methods:GetAttribute(k)return self._attrs[k] end\nfunction methods:SetAttribute(k,v)self._attrs[k]=v end\nfunction methods:GetChildren()local out={} for i,c in ipairs(self._children)do out[i]=c end return out end\nfunction methods:GetDescendants()local out={} for _,c in ipairs(self._children)do out[#out+1]=c;for _,d in ipairs(c:GetDescendants())do out[#out+1]=d end end return out end\nfunction methods:FindFirstChild(name)for _,c in ipairs(self._children)do if c.Name==name then return c end end end\nfunction methods:FindFirstChildOfClass(cls)for _,c in ipairs(self._children)do if c:IsA(cls)then return c end end end\nfunction methods:WaitForChild(name)return self:FindFirstChild(name) end\nfunction methods:FindFirstAncestorOfClass(cls)local p=self.Parent while p do if p:IsA(cls)then return p end p=p.Parent end end\nfunction methods:IsDescendantOf(parent)local p=self.Parent while p do if p==parent then return true end p=p.Parent end return false end\nfunction methods:Destroy()self.Parent=nil;self.destroyed=true end\nfunction methods:SetNetworkOwner(owner)self.serverOwned=owner==nil end\nfunction methods:PivotTo(cf)self.destination=cf;local root=self:FindFirstChild('HumanoidRootPart');if root then root.Position=cf.Position end end\nfunction methods:GetServerTimeNow()return now end\nfunction methods:GetPlayers()return self.playerList end\nfunction methods:GetPlayerFromCharacter(c)for _,p in ipairs(self.playerList)do if p.Character==c then return p end end end\nlocal function node(parent,cls,name)local n=Instance.new(cls);n.Name=name;n.Parent=parent;return n end\nlocal function part(parent,name,x,cls)local p=node(parent,cls or 'Part',name);p.Position=Vector3.new(x or 0,8,0);p.CFrame=CFrame.new(p.Position);p.Size=Vector3.new(14,1,16);return p end\nworkspace=Instance.new('Workspace')\nlocal course=node(workspace,'Folder','ObbyDemo')\nlocal checkpoints=node(course,'Folder','Checkpoints')\nlocal pads={}\nfor i=0,3 do pads[i]=part(checkpoints,tostring(i),i*30,i==0 and 'SpawnLocation' or 'Part') end\nlocal killFolder=node(course,'Folder','KillBlocks');local danger=part(killFolder,'Danger',10)\nlocal movingFolder=node(course,'Folder','MovingPlatforms');local mover=part(movingFolder,'Shuttle',70)\nlocal vanishFolder=node(course,'Folder','DisappearingPlatforms');local tile=part(vanishFolder,'Tile',114)\nlocal finish=part(course,'Finish',120)\nlocal players=Instance.new('Players');players.playerList={}\nlocal server=node(nil,'Folder','ServerScriptService')\nnode(server,'ModuleScript','ObbyCore')\nlocal function character(p)\n local c=node(workspace,'Model',p.Name..'_Character')\n local h=node(c,'Humanoid','Humanoid')\n local r=part(c,'HumanoidRootPart',0)\n p.Character=c\n return c,h,r\nend\nlocal function player(name)\n local p=Instance.new('Player');p.Name=name;p.LocaleId='ru-ru';node(p,'Folder','PlayerGui')\n players.playerList[#players.playerList+1]=p;character(p);return p\nend\nlocal alice,bob=player('Alice'),player('Bob');players.LocalPlayer=alice\nlocal runService=Instance.new('RunService')\nlocal services={Players=players,RunService=runService}\ngame={GetService=function(_,name)assert(services[name],name);return services[name] end}\nlocal function touch(p,pad)p.Character:FindFirstChild('HumanoidRootPart').Position=pad.Position;pad.Touched:Fire(p.Character:FindFirstChild('HumanoidRootPart')) end\nscript={Parent=server}\n"
prelude=prelude.replace('if c.active then c.fn(...) end','if c.active then task.spawn(c.fn, ...) end').replace('runs<1000','runs<100000')
prelude=prelude.replace('return e\nend','function e:Wait() return task.wait(self.duration or 0.01) end\n return e\nend',1)
extra=r'''
os.clock=function() return now end
math.clamp=function(x,a,b)return math.max(a,math.min(b,x))end
math.atan2=math.atan
table.find=function(t,v)for i,x in ipairs(t)do if x==v then return i end end end
vm.__mul=function(a,b)if type(a)=='number'then a,b=b,a end return Vector3.new(a.X*b,a.Y*b,a.Z*b)end
vm.__div=function(a,b)return Vector3.new(a.X/b,a.Y/b,a.Z/b)end
local oldCF=CFrame.new
CFrame.new=function(x,y,z)if type(x)=='number'then return oldCF(Vector3.new(x,y or 0,z or 0))end return oldCF(x or Vector3.zero)end
CFrame.Angles=function()return CFrame.new()end
cm.__mul=function(a,b)return CFrame.new(a.Position+b.Position)end
cm.__index={PointToObjectSpace=function(a,b)return b-a.Position end}
Color3.new=Color3.fromRGB
Random={new=function()return {NextInteger=function(_,a,b)return a end,NextNumber=function(_,a,b)return a or 0.5 end}end}
OverlapParams={new=function()return {}end}
TweenInfo={new=function(seconds)return {seconds=seconds}end}
UDim2.fromScale=UDim2.new;UDim2.fromOffset=UDim2.new
warn=function(...)end
local oldNew=Instance.new
Instance.new=function(cls)
 local n=oldNew(cls)
 n.Enabled=true;n.MaxHealth=100;n.WalkSpeed=16;n.Looped=false;n.IsPlaying=false;n.SoundId='';n.LocalTransparencyModifier=0
 for _,key in ipairs({'Triggered','Destroying','RenderStepped','InputBegan','Activated','TeleportInitFailed','Ended','Completed'})do n._props[key]=event()end
 n.CFrame=CFrame.new();n.Position=Vector3.zero;n.Size=Vector3.new(4,1,4)
 n.AssemblyLinearVelocity=Vector3.zero;n.AssemblyAngularVelocity=Vector3.zero
 return n
end
local oldIsA=methods.IsA
function methods:IsA(cls)
 return oldIsA(self,cls) or cls=='Light' and (self.ClassName=='PointLight' or self.ClassName=='SpotLight' or self.ClassName=='SurfaceLight') or cls=='BasePart' and self.ClassName=='Seat'
end
methods.FindFirstChildWhichIsA=methods.FindFirstChildOfClass
function methods:TakeDamage(amount)self.Health=math.max(0,self.Health-amount)end
function methods:Play()self.IsPlaying=true;self.playCount=(self.playCount or 0)+1 end
function methods:Stop()self.IsPlaying=false end
function methods:Sit(h)self.Occupant=h;h.SeatPart=self end
function methods:Clone()
 local n=Instance.new(self.ClassName)
 for k,v in pairs(self._props)do if type(v)~='table' and k~='Parent' then n[k]=v end end
 for _,c in ipairs(self:GetChildren())do c:Clone().Parent=n end
 return n
end
function methods:GetMouse()return self.mouse end
function methods:GetFocusedTextBox()return self.focused end
function methods:GetPartsInPart()return self.overlaps or {}end
local oldDestroy=methods.Destroy
function methods:Destroy()self.Destroying:Fire();oldDestroy(self)end
local tweenService={Create=function(_,target,info,props)
 local t={Completed=event()};t.Completed.duration=info.seconds
 function t:Play()for k,v in pairs(props)do target[k]=v end end
 return t
end}
local teleports=Instance.new('TeleportService')
function teleports:TeleportAsync(id,list)self.calls=(self.calls or 0)+1;self.lastId=id;if self.fail then error('mock transport failure')end end
local input=Instance.new('UserInputService')
local lighting=Instance.new('Lighting');lighting.ClockTime=12
services.TweenService=tweenService;services.TeleportService=teleports;services.UserInputService=input
services.Lighting=lighting;services.ServerStorage=Instance.new('Folder');services.SoundService=Instance.new('SoundService')
runService.RenderStepped=event()
alice.mouse={};bob.mouse={}
-- Defaults for existing characters created by the inherited fixture.
for _,p in ipairs(players:GetPlayers())do
 local h=p.Character:FindFirstChildOfClass('Humanoid');h.MaxHealth=100;h.WalkSpeed=16
 local root=p.Character:FindFirstChild('HumanoidRootPart');root.AssemblyLinearVelocity=Vector3.zero
 node(p,'Backpack','Backpack')
end
local parent=part(workspace,'TestObject',0, SCRIPT_ID==42 and 'Seat' or 'Part')
parent.CFrame=CFrame.new(parent.Position)
local target=part(workspace,'TargetPart',30)
local destination=part(workspace,'DestinationPart',60)
local folder=node(workspace,'Folder','Destinations')
local randomDestination=part(folder,'RandomDestination',90)
local buttonA=part(workspace,'ButtonA',2);local buttonB=part(workspace,'ButtonB',4)
local light=node(parent,'PointLight','Light');light.Color='white';light.Enabled=true
local sound=node(parent,'Sound','Sound');sound.SoundId='rbxassetid://123';sound.Volume=0.5
local emitter=node(parent,'ParticleEmitter','Particles');emitter.Enabled=true
local function ref(name,value)local n=node(parent,'ObjectValue',name);n.Value=value end
ref('Destination',destination);ref('Destinations',folder);ref('ButtonA',buttonA);ref('ButtonB',buttonB)
ref('Target',SCRIPT_ID==11 and light or target)
local tool=node(services.ServerStorage,'Tool','ToolTemplate')
local zone=part(workspace,'AmbientZone',0);local zoneSound=node(zone,'Sound','Sound');zoneSound.SoundId='rbxassetid://123'
local fade=part(workspace,'FadeObject',0)
local interactables=node(workspace,'Folder','Interactables');local hover=part(interactables,'Hover',0)
local note=part(workspace,'NotePart',0);note:SetAttribute('NoteText','Test note')
local cameraPoint=part(workspace,'CameraPoint',100)
local camera=Instance.new('Camera');camera.CFrame=CFrame.new(0,10,20);camera.CFrame.LookVector=Vector3.new(0,0,-1)
camera.CameraType=Enum.CameraType.Custom;camera.CameraSubject=alice.Character:FindFirstChildOfClass('Humanoid')
workspace.CurrentCamera=camera
script=Instance.new(SCRIPT_ID>=35 and 'LocalScript' or 'Script');script.Parent=parent
local function nearPlayer(p,origin)p.Character:FindFirstChild('HumanoidRootPart').Position=origin.Position end
local function fireTouch(p,object)nearPlayer(p,object);object.Touched:Fire(p.Character:FindFirstChild('HumanoidRootPart'))end
local function use(p,object)nearPlayer(p,object);object:FindFirstChildOfClass('ProximityPrompt').Triggered:Fire(p)end
local function press(key,processed)input.InputBegan:Fire({KeyCode=Enum.KeyCode[key]},processed or false)end
local function root(p)return p.Character:FindFirstChild('HumanoidRootPart')end
local function hum(p)return p.Character:FindFirstChildOfClass('Humanoid')end
'''
# Each script starts with realistic dependencies and executes in its own Lua state.
cases={
1:'''root(alice).Position=Vector3.new(9999,0,0);parent.Touched:Fire(root(alice));eq(alice.Character.destination,nil,'remote touch rejected');fireTouch(alice,parent);near(root(alice).Position.X,60,'teleported');near(root(alice).Position.Y,12.5,'destination clearance');fireTouch(alice,parent);near(root(alice).Position.X,0,'debounce blocks repeat');advance(103);fireTouch(alice,parent);near(root(alice).Position.X,60,'cooldown expires')''',
2:'''root(alice).Position=Vector3.new(9999,0,0);parent:FindFirstChildOfClass('ProximityPrompt').Triggered:Fire(alice);eq(alice.Character.destination,nil,'remote prompt rejected');use(alice,parent);near(root(alice).Position.X,60,'prompt teleported');use(alice,parent);near(root(alice).Position.X,0,'prompt cooldown')''',
3:'''use(alice,parent);near(root(alice).Position.X,90,'random valid destination');use(bob,parent);near(root(bob).Position.X,90,'independent player cooldown')''',
4:'''fireTouch(alice,parent);near(root(alice).Position.X,60,'paired portal move');near(alice:GetAttribute('ToolkitPortalUntil'),103,'shared portal guard');fireTouch(alice,parent);near(root(alice).Position.X,0,'portal repeat guarded')''',
5:'''use(alice,parent);eq(teleports.calls,1,'teleport called');use(alice,parent);eq(teleports.calls,1,'inflight guarded');teleports.TeleportInitFailed:Fire(alice);use(alice,parent);eq(teleports.calls,2,'async failure unlocks');advance(116);teleports.fail=true;use(alice,parent);eq(teleports.calls,3,'timeout unlocks');use(alice,parent);eq(teleports.calls,4,'sync failure unlocks')''',
6:'''use(alice,parent);near(parent.CFrame.Position.Y,17,'door opened');use(alice,parent);near(parent.CFrame.Position.Y,17,'busy rejects reentry');advance(102);use(alice,parent);near(parent.CFrame.Position.Y,8,'door closes')''',
7:'''use(alice,parent);advance(102);use(alice,parent);advance(104);eq(parent.CFrame.Position.Y,8,'hinge toggle restores')''',
8:'''use(alice,parent);near(parent.CFrame.Position.Y,10,'gate open');advance(106);near(parent.CFrame.Position.Y,8,'gate auto closes')''',
9:'''use(alice,parent);near(parent.CFrame.Position.Y,8,'no key denied');node(alice:FindFirstChildOfClass('Backpack'),'Folder','Key');use(alice,parent);near(parent.CFrame.Position.Y,8,'non-tool denied');alice:FindFirstChildOfClass('Backpack'):FindFirstChild('Key'):Destroy();local key=node(alice:FindFirstChildOfClass('Backpack'),'Tool','Key');use(alice,parent);near(parent.CFrame.Position.Y,10,'valid key accepted');advance(107);eq(key.Parent~=nil,true,'key preserved')''',
10:'''use(alice,buttonA);advance(106);use(alice,buttonB);near(parent.CFrame.Position.Y,8,'expired pair denied');use(alice,buttonA);near(parent.CFrame.Position.Y,10,'fresh pair opens');advance(112);near(parent.CFrame.Position.Y,8,'pair gate closes')''',
11:'''use(alice,parent);eq(light.Enabled,false,'light off');use(alice,parent);eq(light.Enabled,true,'light on')''',
12:'''eq(target.Transparency,1,'bridge hidden initially');use(alice,parent);eq(target.CanCollide,true,'bridge active');advance(107);eq(target.CanCollide,false,'bridge expires');eq(target.Transparency,1,'bridge hidden again')''',
13:'''workspace.overlaps={root(alice),root(bob)};nearPlayer(alice,parent);nearPlayer(bob,parent);advance(100.2);eq(target.CanCollide,false,'occupied plate opens');workspace.overlaps={root(bob)};advance(100.4);eq(target.CanCollide,false,'second occupant keeps open');workspace.overlaps={};advance(100.6);eq(target.CanCollide,true,'last exit closes')''',
14:'''use(alice,parent);local first=target.Color;use(alice,parent);eq(first~=target.Color,true,'next color');use(alice,parent);use(alice,parent);eq(target.Color,first,'palette cycles')''',
15:'''local saved=target.CFrame;target.CFrame=CFrame.new(500,0,0);target.AssemblyLinearVelocity=Vector3.new(9,9,9);use(alice,parent);eq(target.CFrame,saved,'reset position');eq(target.AssemblyLinearVelocity,Vector3.zero,'reset velocity')''',
16:'''eq(parent.Anchored,true,'belt anchored');near(parent.AssemblyLinearVelocity.Magnitude,14,'belt surface speed')''',
17:'''fireTouch(alice,parent);near(root(alice).AssemblyLinearVelocity.Y,85,'bounce speed');root(alice).AssemblyLinearVelocity=Vector3.zero;fireTouch(alice,parent);near(root(alice).AssemblyLinearVelocity.Y,0,'bounce debounce')''',
18:'''fireTouch(alice,parent);advance(100.6);eq(parent.CanCollide,false,'tile disappears');fireTouch(bob,parent);advance(103.6);eq(parent.CanCollide,true,'tile restores');eq(parent.Transparency,0,'tile visual restored')''',
19:'''fireTouch(alice,parent);near(parent.CFrame.Position.Y,20,'lift rises');advance(106);near(parent.CFrame.Position.Y,8,'lift returns')''',
20:'''eq(parent.Anchored,false,'shuttle dynamic');eq(parent.serverOwned,true,'server physics ownership');local guide=workspace:FindFirstChild('TestObject_Guide');local servo=guide:FindFirstChildOfClass('PrismaticConstraint');eq(servo.TargetPosition,20,'shuttle outbound');advance(106);eq(servo.TargetPosition,0,'shuttle return target');eq(servo.LimitsEnabled,true,'physical limits')''',
21:'''fireTouch(alice,parent);eq(hum(alice).Health,0,'kill player');eq(hum(bob).Health,100,'other player unchanged')''',
22:'''fireTouch(alice,parent);fireTouch(alice,parent);eq(hum(alice).Health,80,'damage debounced');fireTouch(bob,parent);eq(hum(bob).Health,80,'per player damage');advance(102);fireTouch(alice,parent);eq(hum(alice).Health,60,'damage after cooldown')''',
23:'''hum(alice).Health=98;nearPlayer(alice,parent);workspace.overlaps={root(alice),root(alice)};advance(100.5);eq(hum(alice).Health,100,'heal capped and deduplicated');hum(alice).Health=50;advance(101);eq(hum(alice).Health,54,'one heal per interval')''',
24:'''nearPlayer(alice,parent);workspace.overlaps={root(alice)};advance(100.2);eq(hum(alice).WalkSpeed,7,'slow entered');workspace.overlaps={};advance(100.4);eq(hum(alice).WalkSpeed,16,'speed restored');workspace.overlaps={root(alice)};advance(100.6);hum(alice).WalkSpeed=25;workspace.overlaps={};advance(100.8);eq(hum(alice).WalkSpeed,25,'external speed preserved')''',
25:'''advance(103.1);fireTouch(alice,parent);eq(hum(alice).Health,100,'inactive laser harmless');advance(105.1);fireTouch(alice,parent);eq(hum(alice).Health,0,'active laser damages')''',
26:'''runService.Heartbeat:Fire(30);near(lighting.ClockTime,13,'day speed');lighting.ClockTime=23.9;runService.Heartbeat:Fire(6);near(lighting.ClockTime,0.1,'day wraps')''',
27:'''advance(100.2);eq(type(light.Enabled),'boolean','flicker updates')''',
28:'''nearPlayer(alice,parent);advance(100.3);eq(light.Enabled,true,'near light enabled');root(alice).Position=Vector3.new(999,0,0);root(bob).Position=Vector3.new(999,0,0);advance(100.6);eq(light.Enabled,false,'distant light off')''',
29:'''use(alice,parent);advance(100.3);eq(light.Enabled,false,'alarm flash');use(alice,parent);advance(100.6);eq(light.Color,'white','alarm color restores');eq(light.Enabled,true,'alarm enabled restores')''',
30:'''local first=light.Color;advance(102.1);eq(light.Color~=first,true,'color pulse advances')''',
31:'''eq(sound.IsPlaying,true,'spatial sound playing');eq(sound.Looped,true,'spatial loop enabled');eq(sound.RollOffMaxDistance,60,'spatial distance')''',
32:'''use(alice,parent);use(alice,parent);eq(sound.playCount,1,'no sound restart');sound:Stop();use(alice,parent);eq(sound.playCount,2,'sound playable again')''',
33:'''fireTouch(alice,parent);fireTouch(bob,parent);eq(sound.playCount,1,'touch sound shared debounce');sound:Stop();advance(103);fireTouch(bob,parent);eq(sound.playCount,2,'touch sound cooldown ends')''',
34:'''eq(sound.IsPlaying,true,'playlist started');sound:Stop();advance(101);eq(sound.playCount,2,'playlist selects next');eq(sound.Looped,false,'playlist non-looping')''',
35:'''nearPlayer(alice,zone);advance(100.2);local s=services.SoundService:FindFirstChild('ToolkitAmbientLocal');eq(s.IsPlaying,true,'ambient inside');root(alice).Position=Vector3.new(999,0,0);advance(100.4);eq(s.IsPlaying,false,'ambient outside');eq(zoneSound.IsPlaying,false,'template never globally played')''',
36:'''local first=parent.CFrame;runService.Heartbeat:Fire(0.5);eq(parent.CFrame~=first,true,'rotation callback runs')''',
37:'''runService.Heartbeat:Fire(0.75);near(parent.CFrame.Position.Y,9.5,'bob peak');runService.Heartbeat:Fire(0.75);near(parent.CFrame.Position.Y,8,'bob baseline')''',
38:'''fireTouch(alice,parent);fireTouch(alice,parent);fireTouch(bob,parent);eq(alice:FindFirstChild('leaderstats'):FindFirstChild('ObjectCoins').Value,1,'one reward while collected');eq(bob:FindFirstChild('leaderstats'),nil,'shared coin unavailable');advance(111);fireTouch(bob,parent);eq(bob:FindFirstChild('leaderstats'):FindFirstChild('ObjectCoins').Value,1,'respawn collectible')''',
39:'''camera.CFrame=CFrame.new(fade.Position);runService.RenderStepped:Fire();near(fade.LocalTransparencyModifier,1,'near camera fade');camera.CFrame=CFrame.new(999,0,0);runService.RenderStepped:Fire();near(fade.LocalTransparencyModifier,0,'far fade reset')''',
40:'''alice.mouse.Target=hover;runService.RenderStepped:Fire();local h=workspace:FindFirstChild('ToolkitHover');eq(h.Adornee,hover,'allowed hover highlight');alice.mouse.Target=target;runService.RenderStepped:Fire();eq(h.Adornee,nil,'outside folder ignored')''',
41:'''nearPlayer(alice,note);note:FindFirstChildOfClass('ProximityPrompt').Triggered:Fire(alice);local panel=alice:FindFirstChild('PlayerGui'):FindFirstChild('ToolkitNote'):FindFirstChildOfClass('TextButton');eq(panel.Visible,true,'note opens');eq(panel.Text:find('Test note',1,true)~=nil,true,'note text');panel.Activated:Fire();eq(panel.Visible,false,'note closes');note:FindFirstChildOfClass('ProximityPrompt').Triggered:Fire(alice);root(alice).Position=Vector3.new(999,0,0);runService.Heartbeat:Fire();eq(panel.Visible,false,'note distance closes')''',
42:'''use(alice,parent);eq(parent.Occupant,hum(alice),'seat occupied');use(bob,parent);eq(parent.Occupant,hum(alice),'occupied seat preserved')''',
43:'''fireTouch(alice,parent);eq(parent.Transparency,0,'full health does not consume');hum(alice).Health=80;fireTouch(alice,parent);eq(hum(alice).Health,100,'health capped');eq(parent.Transparency,1,'medkit hidden');hum(bob).Health=50;fireTouch(bob,parent);eq(hum(bob).Health,50,'no double pickup');advance(113);eq(parent.Transparency,0,'medkit respawns')''',
44:'''use(alice,parent);use(alice,parent);eq(#alice:FindFirstChildOfClass('Backpack'):GetChildren(),1,'tool duplicate guarded');eq(alice:FindFirstChildOfClass('Backpack'):FindFirstChild('ToolTemplate'):IsA('Tool'),true,'tool cloned')''',
45:'''eq(emitter.Enabled,false,'particles initially off');use(alice,parent);eq(emitter.Enabled,true,'particles on');use(alice,parent);eq(emitter.Enabled,false,'particles off')''',
46:'''lighting.ClockTime=23.5;runService.Heartbeat:Fire(0.1);local g=alice:FindFirstChild('PlayerGui'):FindFirstChild('ToolkitClock');eq(g:FindFirstChildOfClass('TextLabel').Text,'23:30','clock formats')''',
47:'''runService.RenderStepped:Fire();local label=alice:FindFirstChild('PlayerGui'):FindFirstChild('ToolkitCompass'):FindFirstChildOfClass('TextLabel');eq(label.Text:find('N',1,true),1,'north heading');camera.CFrame.LookVector=Vector3.new(1,0,0);runService.RenderStepped:Fire();eq(label.Text:find('E',1,true),1,'east heading')''',
48:'''root(alice).Position=Vector3.new(1,2,3);runService.Heartbeat:Fire(0.2);local label=alice:FindFirstChild('PlayerGui'):FindFirstChild('ToolkitCoordinates'):FindFirstChildOfClass('TextLabel');eq(label.Text,'X 1.0   Y 2.0   Z 3.0','coordinates format')''',
49:'''local pg=alice:FindFirstChild('PlayerGui');local a=node(pg,'ScreenGui','ToolkitClock');a.Enabled=true;local b=node(pg,'ScreenGui','ToolkitCompass');b.Enabled=false;local other=node(pg,'ScreenGui','Other');press('H',true);eq(a.Enabled,true,'processed input ignored');press('H');eq(a.Enabled,false,'HUD hidden');eq(other.Enabled,true,'unlisted HUD preserved');local later=node(pg,'ScreenGui','ToolkitCoordinates');eq(later.Enabled,false,'late HUD hidden');press('H');eq(a.Enabled,true,'HUD restored');eq(b.Enabled,false,'disabled HUD stays disabled');eq(later.Enabled,true,'late HUD restored')''',
50:'''local previous=camera.CFrame;press('C',true);eq(camera.CameraType,Enum.CameraType.Custom,'processed camera input ignored');press('C');eq(camera.CameraType,Enum.CameraType.Scriptable,'view mode');eq(camera.CFrame,cameraPoint.CFrame,'viewpoint frame');press('C');eq(camera.CameraType,Enum.CameraType.Custom,'camera mode restored');eq(camera.CFrame,previous,'camera frame restored');press('C');alice.CharacterAdded:Fire(alice.Character);eq(camera.CameraType,Enum.CameraType.Custom,'respawn releases camera')'''
}
# Mock CFrame has no orientation math; conveyor needs a look vector.
extra+='\nparent.CFrame.LookVector=Vector3.new(0,0,-1)\n'
failures=[]
for item in items:
 i=item['id'];source=Path(item['path']).read_text()
 if i==5:source=source.replace('local PLACE_ID = 0','local PLACE_ID = 123')
 code=f'local SCRIPT_ID={i}\n'+prelude+extra+'\ntask.spawn(function()\n'+source+'\nend)\n'+cases[i]
 try:execute(code,item['file']);print(f'PASS {i:02d}: startup and behavior')
 except Exception as e:failures.append((i,str(e)));print(f'FAIL {i:02d}: {e}')
if failures:raise SystemExit(f'{len(failures)} cases failed')
assert len({i['file'] for i in items})==50
nodes=ET.parse(P/'ObjectToolkit50.rbxmx').findall('.//Item')
scripts=[n for n in nodes if n.get('class') in ('Script','LocalScript')]
assert len(scripts)==50
for node,item in zip(sorted(scripts,key=lambda n:n.find('./Properties/string[@name="Name"]').text),items):
 assert node.find('./Properties/bool[@name="Disabled"]').text=='true'
 assert node.find('./Properties/ProtectedString[@name="Source"]').text==Path(item['path']).read_text()
checks=sum(case.count('eq(')+case.count('near(') for case in cases.values())
print(f'PASS {checks} behavior assertions; 50 syntax checks; 50 disabled template source parity.')
