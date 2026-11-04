# Roblox Object Toolkit 50 · v1.0.0

**50 самостоятельных скриптов для объектов и игровых механик Roblox Studio.**
**50 standalone scripts for Roblox Studio objects and game mechanics.**

Телепорты · двери · кнопки · платформы · зоны · свет · звук · эффекты · взаимодействия · UI.
Teleports · doors · buttons · platforms · zones · lighting · audio · effects · interactions · UI.

**Автор / Author:** timura032 · **Лицензия / License:** MIT

[Скачать / Download release](https://github.com/Ramzan584/roblox-object-toolkit-50/releases/tag/v1.0.0)

## Быстрый старт · RU

1. Скачай ZIP из Releases и распакуй. Папки архива разделены по категориям.
2. Для `.server.lua` создай обычный **Script**, для `.client.lua` — **LocalScript**. Вставь содержимое нужного файла.
3. Серверные скрипты устанавливай внутрь указанного Part; №26 — в ServerScriptService. Клиентские — в StarterPlayer → StarterPlayerScripts.
4. Создай зависимости из таблицы. **ObjectValue — дочерний объект самого Part**, не Script: задай его Name и перетащи нужный объект в свойство Value. Пример №01: Part A → Destination (ObjectValue) → Value = Part B.
5. Альтернатива: Insert from File → `ObjectToolkit50.rbxmx`. Это библиотека **выключенных шаблонов**. Скопируй выбранный Script/LocalScript в место установки, выполни настройку, затем включи Enabled (или отключи Disabled в старом интерфейсе).
6. Проверь механику через Play и Start Server с двумя игроками, затем на телефоне. Для №05 необходим опубликованный Place и запуск в Roblox-клиенте.

## Quick start · EN

1. Download and extract the release ZIP; category folders preserve organization.
2. Create a **Script** for `.server.lua` or a **LocalScript** for `.client.lua`, then paste the source.
3. Server scripts go inside the specified Part, except #26 in ServerScriptService. Client scripts go in StarterPlayer → StarterPlayerScripts.
4. Create the dependencies in the catalogue. **ObjectValues belong to the Part, not the Script.** Set Name and Value. For #01: Part A → Destination (ObjectValue) → Value = Part B.
5. Or insert `ObjectToolkit50.rbxmx` using Insert from File. All templates are **disabled**. Copy the chosen script to its install location, configure dependencies, then enable it.
6. Test in Studio Play, a two-player local server, and on a phone. #05 requires a published place and Roblox client.

## Проверка и совместимость / Validation and compatibility

This is an initial template release. **Roblox Studio has not been run for this release.** `VALIDATION.txt` lists the automated checks actually performed. Lua-compatible syntax parsing and mocked behavior checks do not validate Roblox physics, replication, audio permissions or mobile controls.

Это начальный выпуск шаблонов. **Реальный запуск в Roblox Studio пока не выполнен.** Подробности автоматической проверки — в `VALIDATION.txt`; движок, физику, репликацию, аудиодоступ и мобильные устройства нужно проверить отдельно.

- Один выбранный скрипт на объект; не включай все 50 сразу. / Install selected behaviors, not the entire library at once.
- Двери и платформы ожидают отдельный Part. Для Model нужна адаптация PivotTo и связей. №19 кинематический; №20 использует физический сервопривод. / Doors and platforms expect a single Part; model support requires adaptation. #19 is kinematic; #20 is physical.
- У сенсоров CanTouch=true; у зон должны быть размеры объёма и queryable части персонажей. / Touch sensors need CanTouch; zones need a volume and queryable character parts.
- Не совмещай контроллеры WalkSpeed, камеры и света без интеграции. №24 не рассчитан на пересекающиеся slow-зоны. / Integrate competing speed, camera and lighting controllers; #24 assumes non-overlapping slow zones.
- №38 — общая монета с респавном, ObjectCoins не сохраняется после выхода. / #38 is a shared respawning coin; ObjectCoins is session-only.
- Звуки не включены: используй свои разрешённые SoundId. В шаблонах камеры/зон при StreamingEnabled обеспечь доступность нужного объекта клиенту. / Supply permitted audio IDs; ensure client target objects are available when streaming is enabled.
- E-подсказки используют стандартный ProximityPrompt, включая сенсорные кнопки. №40 — мышь; №49/50 — клавиатура H/C. / Prompts use built-in touch UI; #40 needs a mouse and #49/#50 need H/C keys.
- Нет executor-кода, HTTP-загрузчиков или сторонних require(assetId). Награды и серверные взаимодействия проверяют живого игрока и расстояние; проверки нужны и при дальнейшей доработке. / No executors, HTTP loaders or third-party asset requires. Server interactions validate living characters and proximity.

## Повторить проверки / Reproduce checks

`python verify_pack.py` — Python 3 + system `liblua5.4.so.0` (Linux). Runs syntax parsing, 50 isolated mock scenarios and template source parity. Does not launch Roblox. / Проверяет синтаксис, 50 сценариев с заглушками и соответствие шаблонов исходникам. Roblox не запускается.

## Каталог / Catalogue

На GitHub исходники лежат в корне для быстрого просмотра; в ZIP они разложены по категориям. / GitHub sources are flat for browsing; ZIP sources use category folders.

### 01 Teleports

| # | Механика / Mechanic | Тип / Type | Установка / Setup |
|---|---|---|---|
| 01 | [Телепорт по касанию / Touch teleport](01_TouchTeleport.server.lua) | Script | Part A: ObjectValue Destination → Part B. |
| 02 | [Телепорт через кнопку E / Prompt teleport](02_PromptTeleport.server.lua) | Script | Part: ObjectValue Destination → Part B. |
| 03 | [Случайная точка / Random destination teleport](03_RandomTeleport.server.lua) | Script | Part: ObjectValue Destinations → Folder с Part / Folder containing destination Parts. |
| 04 | [Двусторонний портал / Paired portals](04_PairedPortal.server.lua) | Script | По копии в A и B; Destination каждого указывает на другой / one copy in each portal, cross-link Destination. |
| 05 | [Переход в другой Place / Teleport to another place](05_PlaceTeleport.server.lua) | Script | Part. PLACE_ID = ID своего опубликованного Place / your published destination ID. Roblox client required. |

### 02 Doors

| # | Механика / Mechanic | Тип / Type | Установка / Setup |
|---|---|---|---|
| 06 | [Раздвижная дверь / Sliding door](06_SlidingDoor.server.lua) | Script | Anchored Part; OFFSET и SECONDS в коде / configure OFFSET and SECONDS. |
| 07 | [Распашная дверь / Hinged door](07_HingedDoor.server.lua) | Script | Anchored Part; петля на левом краю локальной X / hinge at local left edge. |
| 08 | [Ворота с автозакрытием / Timed gate](08_TimedGate.server.lua) | Script | Anchored Part; WAIT_SECONDS задаёт время открытия / open duration. |
| 09 | [Дверь с ключом / Key tool door](09_KeyDoor.server.lua) | Script | Part; Tool с именем Key в Backpack или Character / Tool named Key. Does not consume key. |
| 10 | [Ворота с двумя кнопками / Two button gate](10_TwoButtonGate.server.lua) | Script | Gate Part: ObjectValue ButtonA и ButtonB → разные Part. Нажать за 5 с / press both within 5 seconds. |

### 03 Buttons

| # | Механика / Mechanic | Тип / Type | Установка / Setup |
|---|---|---|---|
| 11 | [Кнопка света / Light switch](11_ToggleLight.server.lua) | Script | Button Part: ObjectValue Target → PointLight, SpotLight или SurfaceLight (Light). |
| 12 | [Временный мост / Timed bridge button](12_TimedBridge.server.lua) | Script | Button Part: ObjectValue Target → Bridge Part; начинается невидимым / starts hidden. |
| 13 | [Нажимная плита / Pressure plate](13_PressurePlate.server.lua) | Script | Plate Part: ObjectValue Target → Gate Part. CanQuery=true у частей персонажа / character parts must be queryable. |
| 14 | [Кнопка смены цвета / Color cycle button](14_ColorCycle.server.lua) | Script | Button Part: ObjectValue Target → Part. |
| 15 | [Возврат объекта на место / Reset movable object](15_ResetObject.server.lua) | Script | Button Part: ObjectValue Target → Part. Сохраняет стартовую CFrame / stores initial CFrame. |

### 04 Platforms

| # | Механика / Mechanic | Тип / Type | Установка / Setup |
|---|---|---|---|
| 16 | [Конвейер / Conveyor belt](16_Conveyor.server.lua) | Script | Anchored Part. DIRECTION и SPEED / direction and speed in code. Unanchored riders. |
| 17 | [Батут / Bounce pad](17_BouncePad.server.lua) | Script | Part. UP_SPEED в studs/sec; CanTouch=true. |
| 18 | [Исчезающая плитка / Disappearing tile](18_DisappearingTile.server.lua) | Script | Anchored Part. Исчезает на 3 с после задержки / vanishes after 0.5 seconds. |
| 19 | [Подъёмная платформа / Rising platform](19_RisingPlatform.server.lua) | Script | Anchored Part. Кинематическая: перенос пассажира не гарантирован / kinematic, rider transport not guaranteed. |
| 20 | [Платформа на физической направляющей / Physical servo shuttle](20_ServoShuttle.server.lua) | Script | Part без Weld/Constraint к миру / no weld to world. Local X axis; TRAVEL, SPEED. Anchors guide, unanchors platform. |

### 05 Zones

| # | Механика / Mechanic | Тип / Type | Установка / Setup |
|---|---|---|---|
| 21 | [Смертельный блок / Kill block](21_KillBlock.server.lua) | Script | Part; CanTouch=true. Убивает только живого игрока рядом / living nearby players only. |
| 22 | [Блок урона / Damage block](22_DamageBlock.server.lua) | Script | Part; DAMAGE и COOLDOWN. Respect ForceField via TakeDamage. |
| 23 | [Зона лечения / Healing zone](23_HealingZone.server.lua) | Script | Volume Part; Anchored=true, CanCollide=false; HEAL_PER_SECOND. Queryable characters. |
| 24 | [Зона замедления / Slow zone](24_SlowZone.server.lua) | Script | Volume Part; CanCollide=false. Один контроллер скорости на Humanoid / avoid overlapping speed controllers. |
| 25 | [Периодический лазер / Timed laser](25_TimedLaser.server.lua) | Script | Part; CanTouch=true. ON_SECONDS / OFF_SECONDS; касание при активном луче / contact while active. |

### 06 Lighting

| # | Механика / Mechanic | Тип / Type | Установка / Setup |
|---|---|---|---|
| 26 | [Цикл дня и ночи / Day night cycle](26_DayNightCycle.server.lua) | Script | Script → ServerScriptService. DAY_MINUTES = длительность суток / real minutes per game day. |
| 27 | [Мерцающая лампа / Flickering light](27_FlickerLight.server.lua) | Script | Part с дочерним PointLight / SpotLight / SurfaceLight. |
| 28 | [Свет при приближении / Proximity lamp](28_ProximityLamp.server.lua) | Script | Part с Light; RADIUS=20. Любой живой игрок в радиусе / any living player nearby. |
| 29 | [Аварийная лампа / Alarm lamp switch](29_AlarmLight.server.lua) | Script | Part с Light. Prompt переключает мигание / toggles flashing. Restores initial color/enabled. |
| 30 | [Плавная смена света / Color pulsing light](30_ColorPulseLight.server.lua) | Script | Part с Light; сначала Enabled=true / enable the Light. |

### 07 Audio

| # | Механика / Mechanic | Тип / Type | Установка / Setup |
|---|---|---|---|
| 31 | [Зацикленный звук объекта / Spatial looping sound](31_SpatialLoop.server.lua) | Script | Part с Sound: свой разрешённый SoundId / permitted audio asset ID. Volume≤1 recommended. |
| 32 | [Звук по кнопке / Prompt sound](32_PromptSound.server.lua) | Script | Part с Sound и своим SoundId / Sound with permitted SoundId. Не перезапускает играющий / no restart while playing. |
| 33 | [Звук по касанию / Touch sound](33_TouchSound.server.lua) | Script | Part с Sound и своим SoundId / Sound with permitted SoundId; global cooldown=2 s. |
| 34 | [Случайный плейлист / Random playlist](34_RandomPlaylist.server.lua) | Script | Part с несколькими Sound / multiple Sounds with permitted SoundIds; track timeout=180 s. |
| 35 | [Локальный звук в зоне / Client ambient zone](35_AmbientZone.client.lua) | LocalScript | LocalScript → StarterPlayerScripts. Workspace: Part AmbientZone с Sound; Anchored=true; copy SoundId. |

### 08 ObjectEffects

| # | Механика / Mechanic | Тип / Type | Установка / Setup |
|---|---|---|---|
| 36 | [Вращающийся декор / Rotating decoration](36_Rotator.server.lua) | Script | Anchored Part; косметика / decoration, not a passenger platform. |
| 37 | [Парящий объект / Bobbing decoration](37_BobbingObject.server.lua) | Script | Anchored Part; AMPLITUDE=1.5, PERIOD=3. Cosmetic. |
| 38 | [Собираемая монета / Collectible coin](38_CollectibleCoin.server.lua) | Script | Part; начисляет ObjectCoins в leaderstats на текущую сессию / session-only reward. Shared respawn 10 s. |
| 39 | [Прозрачность вблизи камеры / Camera distance fade](39_DistanceFade.client.lua) | LocalScript | LocalScript → StarterPlayerScripts. Workspace Part FadeObject. Только один Part / affects one part. |
| 40 | [Подсветка при наведении / Mouse hover highlight](40_HoverHighlight.client.lua) | LocalScript | LocalScript → StarterPlayerScripts. Workspace Folder Interactables с Part/Model. Mouse only. |

### 09 Interactions

| # | Механика / Mechanic | Тип / Type | Установка / Setup |
|---|---|---|---|
| 41 | [Чтение записки / Readable note](41_ReadNote.client.lua) | LocalScript | LocalScript → StarterPlayerScripts. Workspace Part NotePart; attribute NoteText (string). Local UI, auto-close beyond 16 studs. |
| 42 | [Сесть по кнопке / Seat prompt](42_SeatPrompt.server.lua) | Script | Script → Seat (не обычный Part / must be Seat). |
| 43 | [Аптечка / Health pickup](43_HealthPickup.server.lua) | Script | Part; HEAL=35; shared respawn 12 seconds. Не расходуется при полном здоровье / stays for full-health players. |
| 44 | [Выдача инструмента / Tool dispenser](44_ToolDispenser.server.lua) | Script | Part; ServerStorage.ToolTemplate (Tool). Свой безопасный Tool / use your own trusted Tool. No duplicates. |
| 45 | [Переключение частиц / Particle toggle](45_ToggleParticles.server.lua) | Script | Part с ParticleEmitter внутри / ParticleEmitters in descendants. Prompt toggles all. |

### 10 ClientUI

| # | Механика / Mechanic | Тип / Type | Установка / Setup |
|---|---|---|---|
| 46 | [Игровые часы / Game clock HUD](46_GameClock.client.lua) | LocalScript | LocalScript → StarterPlayerScripts; отображает Lighting.ClockTime / displays game time. |
| 47 | [Компас / Compass HUD](47_Compass.client.lua) | LocalScript | LocalScript → StarterPlayerScripts. Север = -Z / North = -Z; camera-based. |
| 48 | [Координаты игрока / Player coordinates HUD](48_Coordinates.client.lua) | LocalScript | LocalScript → StarterPlayerScripts. X/Y/Z; для строительства и отладки / building/debug HUD. |
| 49 | [Скрыть интерфейс клавишей H / HUD toggle key](49_HUDToggle.client.lua) | LocalScript | LocalScript → StarterPlayerScripts. TARGETS: имена своих ScreenGui / your ScreenGui names. Keyboard H. |
| 50 | [Камера наблюдения / Camera viewpoint toggle](50_CameraViewpoint.client.lua) | LocalScript | LocalScript → StarterPlayerScripts. Workspace anchored Part CameraPoint. C toggle, repeats on respawn. Keyboard. |

## Официальная документация / Official documentation

- [Script locations](https://create.roblox.com/docs/scripting/locations)
- [Proximity prompts](https://create.roblox.com/docs/ui/proximity-prompts)
- [Client-server security](https://create.roblox.com/docs/scripting/security/client-server-boundary)
- [Teleport between places](https://create.roblox.com/docs/projects/teleport)
- [PrismaticConstraint](https://create.roblox.com/docs/reference/engine/classes/PrismaticConstraint)

Об ошибках: создай Issue с номером скрипта, местом установки, шагами воспроизведения и сообщением Output. / Report issues with script number, install location, reproduction steps and Output errors.
