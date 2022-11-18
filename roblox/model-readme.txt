--  _____  ______   ________          _          __   ___  
-- |  __ \|  _ \ \ / /  ____|        | |        /_ | / _ \ 
-- | |__) | |_) \ V /| |__ ___  _ __ | |_  __   _| || | | |
-- |  _  /|  _ < > < |  __/ _ \| '_ \| __| \ \ / / || | | |
-- | | \ \| |_) / . \| | | (_) | | | | |_   \ V /| || |_| |
-- |_|  \_\____/_/ \_\_|  \___/|_| |_|\__|   \_/ |_(_)___/ 
--
-- https://github.com/oxi-dev0/RBXFont

-------------------------------------------------
-- SETUP

-- Move 'Ungroup-In-ReplicatedStorage' to game.ReplicatedStorage, right click it and press Ungroup. This folder "RBXFonts" contains definitions for all fonts used by the system, and is referenced directly, so dont rename it.
-- Move 'RBXFontLabel' to wherever you want to use the label. Feel free to change any of it's parameters.
-- Read the rest of this README to understand how to use the system.

-------------------------------------------------

-------------------------------------------------
-- QUICK EXPLANATION

-- Fonts are defined in game.ReplicatedStorage.RBXFonts
-- Text parameters are defined as attributes on the RBXFont script under the RBXFontLabel

-- Please read the RBXFont script to understand the attributes and the system.

-- The RBXFont script automatically generates the text on start.
-- The RBXFont script requires the RBXFontLabel as it's parent.
-- For FX to work, please set the parent GUI's ZIndexBehaviour to Global

-- THIS SYSTEM ONLY WORKS FOR MONOSPACED FONTS!

-------------------------------------------------

-------------------------------------------------
-- API

-- LoadFont - loads the configuration from the font module, and regenerates the UI if already generated. Specify the font module by changing the font variable. Create font modules in ReplicatedStorage.RBXCustomFonts
-- Generate - generates the actual UI for the text. if already generated, the UI will be cleared before it is generated.
-- Clear - removes any generated UI and resets any frame sizes.

-------------------------------------------------

-------------------------------------------------
-- FEATURES

-- Quick custom fonts: Using the python script found on the system's Github page (https://github.com/oxi-dev0/RBXFont), fontsheet images and font ModuleScripts can be generated in a couple seconds.
-- Low overhead: The text is only generated as needed, and does not eat up resources.
-- Lots of customisation: The system contains many visual features such as Wrapping, Padding and Alignment. All of these features can be customised as needed by attributes on the RBXFont script
-- Effects system: Effects can be stacked on top of the text how ever many times as needed, allowing for advanced looks such as Chromatic Abberation through mutiple offset Outline Effects.

-------------------------------------------------

-------------------------------------------------
-- UPCOMING

-- More effect types
-- More customisation options such as allowing a higher maximum width than what is set at start-time
-- Better optimisation and readability of the core script
-- More example fonts

------------------------------------------------