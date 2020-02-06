## Outfit Customization (OC) by ColonolNutty

For more mods like this support me at my Patreon: https://www.patreon.com/colonolnutty

### Features:

- Customize clothing pieces/accessories your sim is wearing without going into CAS
  - Put on or Take off clothing items on the fly
    - Example: Put On/Take Off Glasses without hassle! (This mod does not come with glasses, get your own!)
    - Extensible: You can add your own clothing items to work with this mod without needing to modify the CAS item itself. (Modders, see below)
 

### Planned Features:

- Update the Dialog to be more like a "Sim" picker visually (although you'd be picking cas parts instead)
  - Enable Outfit Customization for children and toddlers
  - The Bulge will NOT be enabled and OC will take no responsibility for what people decide to add after this change
  - If you ask me to add a Crotch Bulge for them, you will be reported!
- Add the ability to add a part to ALL outfits of a sim.
- Add the ability to remove a part from ALL outfits of a sim.
- Add Outfit Sets to enable equipping/unequipping entire sets of clothing
  - Custom Set names
  - Add/Remove cas parts from each set
  - Specify the slot to equip a cas part in
 

### Mods that add to this:

- Do let me know in the support thread or the discord if you add stuff to this mod and I can link it here!
  - Just remember that OC is by itself a Non-Adult mod and breaks no rules, however linked content may or may not break LL rules depending on what said linked content adds to OC, OC is not responsible for the content that mod authors add to it. If linked content does break LL rules, please bring it to my attention and I will unlink it from the description
  - [Crilender](https://crilender.tumblr.com/outfitcustomizationmod) - Various vanilla cas parts.

### Mod Settings (Mod Usage):

- Customize Outfit
  - Click a Sim that is of age Teen, Young Adult, Adult, or Elder
  - Locate the Customize Outfit (OC) interaction (It shows up as a top level interaction, it has OC in the name, so you know its from this mod)
  - Choose what you want to put on/take off
  - The items you have on already show up as green.
 

### Installation:

- Download and install The Sims 4 Community Library (link in the Requirements section)
- Download this mod (When downloading, it's the one without a name)
- Unpack the this mods archive and drop the files from it into your Mods folder (...\The Sims 4\Mods\)
- Enjoy

 

### Translations:

- None so far.
 

### Requirements:

- Sims 4 version 1.56.52.1020 (Realm of Magic patch) or above
- The latest version of [The Sims 4 Community Library](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases)
 

### Vanilla CAS Part Progress:

- Progress Colors (Not Done/Not In Progress (Red), In Progress (Yellow), Done (Green))
- Clothing
  - Head wear
  - Shoes
  - Accessories
  - Glasses
  - Gloves
  - Earrings
  - Wrist
  - Rings
 

 

### General Troubleshooting Steps:

- Step One:
  - Ensure you have the Custom Scripts option enabled in-game in the settings
  - If you get a corrupted file error while unzipping, update the version of your 7-zip and start over
  - Verify, that you have fulfilled all of the requirements
  - Verify, that you have completed all of the steps in the installation process
  - If all of the above checks out, move to Step Two- Step Two:
  - Rename your "Documents\Electronic Arts\The Sims 4" folder to "Documents\Electronic Arts\The Sims 4.bak"
    - You can always recreate your existing game by deleting the "Documents\Electronic Arts\The Sims 4" folder and renaming "Documents\Electronic Arts\The Sims 4.bak" to "Documents\Electronic Arts\The Sims 4"
  - Start Sims 4 and create a simple household with an Adult, a Teen, and a Pet (Cat or Dog, if you can)
  - Save and exit the game
  - Download and install the mod you are trying to get working
  - Start the game with the household you created above
    - Does the problem persist?
      - Yes:
        - Go to the next step
      - No:
        - You have some other mod or a bad save that is causing you problems
- Step Three:
  - Add your other mods one by one
    - Does the problem persist?
      - Yes:
        - You've found the mod that causes things to break, report it to the author of that mod
      - No:
        - Continue adding mods one by one until the problem begins to appear
        - If you've run out of mods to add, then it was probably just a fluke in the system.
- Problem Reporting Steps:
  - Follow the troubleshooting steps above BEFORE following these steps
  - Post in the thread the following details:
    - Upload the following files, if they exist, they are located in the `Documents\Electronic Arts\The Sims 4` folder
      - REQUIRED IF YOU HAVE AN ORANGE NOTIFICATION BOX IN-GAME
      - The lastexception.txt (lastexception) file
      - The `<Mod Name>_Messages.txt (<Mod Name>_Messages)` file
      - The `<Mod Name>_Exceptions.txt (<Mod Name>_Exceptions)` file
    - A detailed description of the problem (Or your best guess)
      - The steps you take that leads you to the problem or a best guess of what you were doing at the time of the error  
      - Example: I clicked on the fridge to make a sim grab a plate of leftovers then they put it down and immediately began doing flips.
    - Your current Sims 4 version
    - The sims you are having problems with (Adult, Teen, Pet, etc.)
  - Things that will NOT help me solve your problem:
    - A screenshot of the orange "error" text box you get in-game telling you there is a problem
      - This does not contain any useful information other than it telling you there was a problem and a file was created
    - A generic statement "I has problem, fix it please!"
      - I don't know what your problem is or if it is even related to this mod (I'm not a psychiatrist or a mind reader!)
    - A statement such as "I had a problem with your mod, so I uninstalled it, just wanted to let you know"
      - This doesn't help anyone and is very rude (Even if you didn't mean to come off that way)

### For Modders:

- In order for you to add your own parts to this mod, you simply need to know the CAS Part Id (The decimal identifier, not the hex identifier) of your CasPart (You can use Sims 4 Studio to find this out):
- Create a Snippet Tuning in your package file and have it look like the following.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--Ensure your snippet file has this at the top-->
<I c="OCOutfitPartsCollection" i="snippet" m="cnoutfitcustomization.outfit_parts.outfit_parts_collection" n="CN_OC_Example_Parts" s="...">
  <L n="outfit_parts_list">
    <U>
      <!--A String Table Key, this will display on the part on the part in the Customize Outfit dialog.-->
      <T n="part_display_name">0x00000000</T>
      <!--Raw Text to denote the display name of the part, it is used when filtering, it isn't actually displayed.-->
      <T n="part_raw_display_name">Example Name</T>
      <!--Raw Text denoting the author of this Outfit Part.-->
      <T n="part_author">ColonolNutty</T>
      <!-- Numerical Identifier of an icon to use for the part. This should be pointing at a DST Image that is 56x56 pixels in size.-->
      <T n="part_icon_id">678910</T>
      <!--Numerical Identifier of a CAS part, the Type of the tuning file is CAS Part in Sims 4 Studio.-->
      <T n="part_id">12345678</T>
      <!-- Genders this part is available for. See Genders enum.-->
	  <L n="available_for_genders">
	    <E>FEMALE</E>
	  </L>
      <!-- Ages this part is available for. See Ages enum.-->
	  <L n="available_for_ages">
	    <E>TEEN</E>
	    <E>YOUNGADULT</E>
	    <E>ADULT</E>
	    <E>ELDER</E>
	  </L>
      <!-- Species this part is available for. See s4cl.CommonSpecies enum.-->
	  <L n="available_for_species">
	    <E>HUMAN</E>
	  </L>
      <!-- Tags used for filtering (These are dynamic, so they can be anything, try to stick to some kind of community standard though, otherwise we'll end up with a billion of these) (example tags: OTHER, PROP, TONGUE, BODY_PART, GLASSES, etc.)-->
	  <L n="part_tags">
	    <E>OTHER</E>
	    <E>BODY_PART</E>
	  </L>
    </U>
    <U>
      <!--Example of another part-->
      <T n="part_display_name">...</T>
      ...
    </U>
  </L>
</I>
```

### DISCLAIMERS:

- ColonolNutty and the Outfit Customization mod itself are neither responsible, liable, nor accountable for what people use this mod for, what people add to it, or how people extend from it. The accountability is entirely on the third party.
​
### Copyright:

Outfit Customization is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY