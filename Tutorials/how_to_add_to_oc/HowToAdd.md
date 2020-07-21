# How To Add Your Own CAS Parts To Outfit Customization (OC)

## Tools
This is a tutorial on adding your own custom CAS Parts to be usable with the Outfit Customization mod
In order to follow this tutorial, you will need a few tools installed.

- Sims 4 Studio - This is the tool that most of the work will be done in. It will be used to create, open, and modify your package file.
- An Image Editor - Prefer an image editor that can rescale the size of images. [Gimp](https://www.gimp.org/) is one such tool you may use.


## Snippet Tuning:

- Create a Snippet Tuning in your package file and have it look similar to the following. We will fill out the pieces further on in the tutorial.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--Ensure your snippet file has this at the top-->
<I c="OCOutfitPartsCollection" i="snippet" m="cnoutfitcustomization.outfit_parts.outfit_parts_collection" n="CN_OC_Example_Parts" s="...">
  <L n="outfit_parts_list">
    <U>
      <!--A String Table Key, this will display on the part in the Customize Outfit dialog.-->
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
        <E>GLASSES</E>
        <E>HEADWEAR</E>
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
### Elements:
| Element Name | Description | Type |
| ------------ | ----------- | ---- |
| part_display_name | The name of the part that will display in the Outfit Customization dialog. | A Hexadecimal value pointing to text within in a String Table within the package file. |
| part_raw_display_name | The name of the part, used when sorting CAS parts alphabetically in the OC dialog. | A Raw String value. |
| part_author | The name of the author of the part. | A String value |
| part_icon_id | The identifier for the image of the CAS part when displayed in the OC dialog. (See "How Do To Create a CAS Part Icon?" below) | A Decimal identifier pointing to a DST image within the package file. |
| part_id | The Decimal identifier for the image of the CAS part. (See "Where Can I Find The Decimal Identifier of a Tuning File?" below) | A Decimal identifier pointing to a CAS Part within the package file. |
| available_for_genders | A collection of Genders the CAS part will be available for. | A collection of `sims.sim_info_types.Gender` enum values. |
| available_for_ages | A collection of Ages the CAS part will be available for. | A collection of `sims.sim_info_types.Age` enum values. |
| available_for_species | A collection of Species the CAS part will be available for. | A collection of [sims4communitylib.enums.CommonSpecies](https://sims4communitylibrary.readthedocs.io/en/latest/sims4communitylib.enums.html#species) enum values. |
| part_tags | A collection of dynamic tags to be more specific with the CAS part. | A collection of raw text tags, they can be anything you wish. |

## Where Can I Find The Decimal Identifier of a Tuning File? (part_id)
1. Follow the steps listed [[here|Where To Find The Decimal Identifier Of A Tuning File]]
2. Once you have your Decimal Identifier, paste it within `part_id`.

## How Do You Create a CAS Part Icon? (part_icon_id)
1. Follow the steps listed [[here|How To Create An Icon]]
2. Once you have your Decimal Identifier, paste it within `part_icon_id`.