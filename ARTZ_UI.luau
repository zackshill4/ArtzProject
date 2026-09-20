--!strict
-- ARTZ UI
-- Luau / Roblox Studio
-- Put this LocalScript in StarterPlayer > StarterPlayerScripts

local Players = game:GetService("Players")
local UserInputService = game:GetService("UserInputService")
local TweenService = game:GetService("TweenService")

local player = Players.LocalPlayer
local playerGui = player:WaitForChild("PlayerGui")

local old = playerGui:FindFirstChild("ARTZ_UI")
if old then
	old:Destroy()
end

local COLORS = {
	Background = Color3.fromRGB(8, 9, 13),
	Panel = Color3.fromRGB(13, 15, 21),
	Panel2 = Color3.fromRGB(18, 20, 28),
	Text = Color3.fromRGB(230, 230, 238),
	Muted = Color3.fromRGB(105, 110, 125),
	Border = Color3.fromRGB(35, 38, 49),
	Accent = Color3.fromRGB(145, 92, 255),
}

local function addCorner(instance: Instance, radius: number)
	local corner = Instance.new("UICorner")
	corner.CornerRadius = UDim.new(0, radius)
	corner.Parent = instance
	return corner
end

local function addStroke(instance: Instance)
	local stroke = Instance.new("UIStroke")
	stroke.Color = COLORS.Border
	stroke.Thickness = 1
	stroke.Parent = instance
	return stroke
end

local function makeLabel(
	parent: Instance,
	text: string,
	size: UDim2,
	position: UDim2,
	textSize: number,
	color: Color3,
	font: Enum.Font
)
	local label = Instance.new("TextLabel")
	label.BackgroundTransparency = 1
	label.Size = size
	label.Position = position
	label.Text = text
	label.TextSize = textSize
	label.TextColor3 = color
	label.Font = font
	label.TextXAlignment = Enum.TextXAlignment.Left
	label.Parent = parent
	return label
end

local window = Instance.new("Frame")
window.Name = "Window"
window.AnchorPoint = Vector2.new(0.5, 0.5)
window.Position = UDim2.fromScale(0.5, 0.5)
window.Size = UDim2.fromOffset(680, 430)
window.BackgroundColor3 = COLORS.Background
window.BorderSizePixel = 0
window.Parent = gui

addCorner(window, 9)
addStroke(window)

local header = Instance.new("Frame")
header.Name = "Header"
header.Size = UDim2.new(1, 0, 0, 54)
header.BackgroundColor3 = COLORS.Panel
header.BorderSizePixel = 0
header.Parent = window
addCorner(header, 9)

makeLabel(
	header,
	"ARTZ",
	UDim2.fromOffset(150, 24),
	UDim2.fromOffset(18, 7),
	21,
	COLORS.Text,
	Enum.Font.GothamBlack
)

makeLabel(
	header,
	"TACTICAL CONTROL",
	UDim2.fromOffset(180, 16),
	UDim2.fromOffset(19, 32),
	9,
	COLORS.Muted,
	Enum.Font.GothamMedium
)

local collapseButton = Instance.new("TextButton")
collapseButton.Size = UDim2.fromOffset(32, 30)
collapseButton.Position = UDim2.new(1, -48, 0.5, -15)
collapseButton.BackgroundColor3 = COLORS.Panel2
collapseButton.Text = "—"
collapseButton.TextColor3 = COLORS.Muted
collapseButton.TextSize = 16
collapseButton.Font = Enum.Font.GothamBold
collapseButton.BorderSizePixel = 0
collapseButton.Parent = header
addCorner(collapseButton, 6)

local dragging = false
local dragStart = Vector2.zero
local startPosition = window.Position

header.InputBegan:Connect(function(input)
	if input.UserInputType == Enum.UserInputType.MouseButton1
		or input.UserInputType == Enum.UserInputType.Touch then
		dragging = true
		dragStart = input.Position
		startPosition = window.Position
	end
end)

header.InputEnded:Connect(function(input)
	if input.UserInputType == Enum.UserInputType.MouseButton1
		or input.UserInputType == Enum.UserInputType.Touch then
		dragging = false
	end
end)

UserInputService.InputChanged:Connect(function(input)
	if not dragging then
		return
	end

	if input.UserInputType ~= Enum.UserInputType.MouseMovement
		and input.UserInputType ~= Enum.UserInputType.Touch then
		return
	end

	local delta = input.Position - dragStart

	window.Position = UDim2.new(
		startPosition.X.Scale,
		startPosition.X.Offset + delta.X,
		startPosition.Y.Scale,
		startPosition.Y.Offset + delta.Y
	)
end)

local sidebar = Instance.new("Frame")
sidebar.Name = "Sidebar"
sidebar.Position = UDim2.fromOffset(12, 66)
sidebar.Size = UDim2.fromOffset(150, 350)
sidebar.BackgroundColor3 = COLORS.Panel
sidebar.BorderSizePixel = 0
sidebar.Parent = window
addCorner(sidebar, 7)
addStroke(sidebar)

local content = Instance.new("Frame")
content.Name = "Content"
content.Position = UDim2.fromOffset(174, 66)
content.Size = UDim2.new(1, -186, 1, -78)
content.BackgroundTransparency = 1
content.Parent = window

local pages: {[string]: ScrollingFrame} = {}
local buttons: {[string]: TextButton} = {}

local function createPage(name: string)
	local page = Instance.new("ScrollingFrame")
	page.Name = name .. "Page"
	page.Size = UDim2.fromScale(1, 1)
	page.BackgroundTransparency = 1
	page.BorderSizePixel = 0
	page.ScrollBarThickness = 3
	page.ScrollBarImageColor3 = COLORS.Accent
	page.CanvasSize = UDim2.fromOffset(0, 0)
	page.Visible = false
	page.Parent = content

	local layout = Instance.new("UIListLayout")
	layout.Padding = UDim.new(0, 8)
	layout.SortOrder = Enum.SortOrder.LayoutOrder
	layout.Parent = page

	layout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
		page.CanvasSize = UDim2.fromOffset(
			0,
			layout.AbsoluteContentSize.Y + 12
		)
	end)

	pages[name] = page
	return page
end

local function createTab(name: string, order: number)
	local button = Instance.new("TextButton")
	button.Name = name .. "Button"
	button.Position = UDim2.fromOffset(8, 8 + ((order - 1) * 45))
	button.Size = UDim2.new(1, -16, 0, 38)
	button.BackgroundColor3 = COLORS.Panel
	button.Text = "  " .. name
	button.TextColor3 = COLORS.Muted
	button.TextSize = 11
	button.Font = Enum.Font.GothamBold
	button.TextXAlignment = Enum.TextXAlignment.Left
	button.BorderSizePixel = 0
	button.Parent = sidebar

	addCorner(button, 6)
	buttons[name] = button
	return button
end

local function createSection(parent: ScrollingFrame, text: string)
	local frame = Instance.new("Frame")
	frame.Size = UDim2.new(1, -8, 0, 40)
	frame.BackgroundColor3 = COLORS.Panel2
	frame.BorderSizePixel = 0
	frame.Parent = parent

	addCorner(frame, 6)

	makeLabel(
		frame,
		text,
		UDim2.new(1, -20, 1, 0),
		UDim2.fromOffset(12, 0),
		10,
		COLORS.Text,
		Enum.Font.GothamBold
	)

	return frame
end

local function createToggle(
	parent: ScrollingFrame,
	text: string,
	defaultState: boolean
)
	local row = Instance.new("Frame")
	row.Size = UDim2.new(1, -8, 0, 44)
	row.BackgroundColor3 = COLORS.Panel
	row.BorderSizePixel = 0
	row.Parent = parent

	addCorner(row, 6)

	makeLabel(
		row,
		text,
		UDim2.new(1, -70, 1, 0),
		UDim2.fromOffset(12, 0),
		11,
		COLORS.Text,
		Enum.Font.GothamMedium
	)

	local toggle = Instance.new("TextButton")
	toggle.Size = UDim2.fromOffset(42, 22)
	toggle.Position = UDim2.new(1, -54, 0.5, -11)
	toggle.BackgroundColor3 = COLORS.Panel2
	toggle.Text = ""
	toggle.BorderSizePixel = 0
	toggle.Parent = row

	addCorner(toggle, 12)

	local knob = Instance.new("Frame")
	knob.Size = UDim2.fromOffset(16, 16)
	knob.BackgroundColor3 = Color3.fromRGB(245, 245, 245)
	knob.BorderSizePixel = 0
	knob.Parent = toggle
	addCorner(knob, 8)

	local state = defaultState

	local function update()
		if state then
			toggle.BackgroundColor3 = COLORS.Accent
			knob.Position = UDim2.new(1, -19, 0.5, -8)
		else
			toggle.BackgroundColor3 = COLORS.Panel2
			knob.Position = UDim2.new(0, 3, 0.5, -8)
		end
	end

	update()

	toggle.Activated:Connect(function()
		state = not state

		TweenService:Create(
			toggle,
			TweenInfo.new(0.12),
			{BackgroundColor3 = state and COLORS.Accent or COLORS.Panel2}
		):Play()

		TweenService:Create(
			knob,
			TweenInfo.new(0.12),
			{
				Position = state
					and UDim2.new(1, -19, 0.5, -8)
					or UDim2.new(0, 3, 0.5, -8)
			}
		):Play()
	end)

	return row
end

local function createSlider(
	parent: ScrollingFrame,
	text: string,
	minimum: number,
	maximum: number,
	initial: number
)
	local row = Instance.new("Frame")
	row.Size = UDim2.new(1, -8, 0, 64)
	row.BackgroundColor3 = COLORS.Panel
	row.BorderSizePixel = 0
	row.Parent = parent

	addCorner(row, 6)

	makeLabel(
		row,
		text,
		UDim2.new(1, -90, 0, 20),
		UDim2.fromOffset(12, 7),
		11,
		COLORS.Text,
		Enum.Font.GothamMedium
	)

	local valueLabel = makeLabel(
		row,
		tostring(initial),
		UDim2.fromOffset(70, 20),
		UDim2.new(1, -82, 0, 7),
		11,
		COLORS.Accent,
		Enum.Font.GothamBold
	)

	valueLabel.TextXAlignment = Enum.TextXAlignment.Right

	local track = Instance.new("TextButton")
	track.Size = UDim2.new(1, -24, 0, 6)
	track.Position = UDim2.fromOffset(12, 40)
	track.BackgroundColor3 = Color3.fromRGB(35, 37, 47)
	track.Text = ""
	track.BorderSizePixel = 0
	track.Parent = row
	addCorner(track, 3)

	local fill = Instance.new("Frame")
	fill.Size = UDim2.fromScale(
		math.clamp((initial - minimum) / (maximum - minimum), 0, 1),
		1
	)
	fill.BackgroundColor3 = COLORS.Accent
	fill.BorderSizePixel = 0
	fill.Parent = track
	addCorner(fill, 3)

	track.Activated:Connect(function(input)
		local mouseX = input.Position.X
		local startX = track.AbsolutePosition.X
		local width = track.AbsoluteSize.X

		local ratio = math.clamp((mouseX - startX) / width, 0, 1)
		local value = math.floor(minimum + ((maximum - minimum) * ratio))

		valueLabel.Text = tostring(value)
		fill.Size = UDim2.fromScale(ratio, 1)
	end)

	return row
end

createTab("AIM", 1)
local aimPage = createPage("AIM")
createSection(aimPage, "AIM SETTINGS")
createToggle(aimPage, "Aim Assist", false)
createSlider(aimPage, "FOV", 10, 360, 120)
createSlider(aimPage, "Smoothness", 0, 100, 35)
createSection(aimPage, "TARGET")
createToggle(aimPage, "Team Check", true)
createToggle(aimPage, "Visibility Check", true)

createTab("ESP", 2)
local espPage = createPage("ESP")
createSection(espPage, "PLAYER ESP")
createToggle(espPage, "ESP Enabled", false)
createToggle(espPage, "Box", true)
createToggle(espPage, "Name", true)
createToggle(espPage, "Health", true)
createToggle(espPage, "Distance", false)

createTab("VISUALS", 3)
local visualsPage = createPage("VISUALS")
createSection(visualsPage, "VISUAL SETTINGS")
createToggle(visualsPage, "FOV Circle", true)
createToggle(visualsPage, "Tracers", false)
createToggle(visualsPage, "Highlights", false)

createTab("SETTINGS", 4)
local settingsPage = createPage("SETTINGS")
createSection(settingsPage, "INTERFACE")
createToggle(settingsPage, "Animations", true)
createToggle(settingsPage, "Remember Position", true)
createSection(settingsPage, "ABOUT")

makeLabel(
	settingsPage,
	"ARTZ  •  Artz  •  GTW_aaaa  •  v1.0.0",
	UDim2.new(1, -8, 0, 44),
	UDim2.fromOffset(0, 0),
	10,
	COLORS.Muted,
	Enum.Font.GothamMedium
)

local function selectTab(name: string)
	for tabName, button in pairs(buttons) do
		local selected = tabName == name

		button.BackgroundColor3 = selected
			and Color3.fromRGB(28, 23, 42)
			or COLORS.Panel

		button.TextColor3 = selected
			and COLORS.Accent
			or COLORS.Muted
	end

	for pageName, page in pairs(pages) do
		page.Visible = pageName == name

		if page.Visible then
			page.CanvasPosition = Vector2.zero
		end
	end
end

for name, button in pairs(buttons) do
	button.Activated:Connect(function()
		selectTab(name)
	end)
end

selectTab("AIM")

local expanded = true

collapseButton.Activated:Connect(function()
	expanded = not expanded

	if expanded then
		window.Size = UDim2.fromOffset(680, 430)
		sidebar.Visible = true
		content.Visible = true
	else
		window.Size = UDim2.fromOffset(680, 54)
		sidebar.Visible = false
		content.Visible = false
	end
end)

print("[ARTZ] UI loaded successfully")
