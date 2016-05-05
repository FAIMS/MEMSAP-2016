#!/usr/bin/env bash

cd module

# Delete autogenerated onClickUserLogin definition.
string="
onClickUserLogin () {
  \/\/ TODO: Add some things which should happen when this element is clicked
  newTab(\"Control\", true);
}"
replacement=""
perl -0777 -i.original -pe "s/\\Q$string/$replacement/igs" ui_logic.bsh

# Delete autogenerated onClickContextUpdateTexture definition.
string="
onClickContextUpdateTexture () {
  \/\/ TODO: Add some things which should happen when this element is clicked
  newTab(\"Context\/Deposit\", true);
}"
replacement=""
perl -0777 -i.original -pe "s/\\Q$string/$replacement/igs" ui_logic.bsh

# I hate this regex so much. Anyway, what it does is match everything in the
# function definition of `newContext`, including the name, parens and opening
# curly brace, but excluding the closing curly brace. This allows us to stick
# a line right before the closing curly brace.
string="(newContext\\(\\){((?!\\n}).)+)"
replacement="\\1
  copyTargetSpitThickness();"
perl -0777 -i.original -pe "s/$string/$replacement/igs" ui_logic.bsh

# Code to inherit LOT_ID from Context into Sample
string="
  parentTabgroup = tabgroup;
  newSample();"
replacement="
  parentTabgroup   = tabgroup;
  parentTabgroup__ = tabgroup;
  newSample();
  if (parentTabgroup__.equals(\"Context\"))
      copyLotId();"
perl -0777 -i.original -pe "s/\\Q$string/$replacement/igs" ui_logic.bsh

# Link Start_Depth_Magnitude to data schema as measure
string="<input ref=\"Start_Depth_Magnitude\""
replacement="$string faims_attribute_type=\"measure\""
perl -0777 -i.original -pe "s/\\Q$string/$replacement/igs" ui_schema.xml

# Delete autogenerated onClickContextUpdateTexture definition.
string="
onClickContextUpdateTexture () {
  \/\/ TODO: Add some things which should happen when this element is clicked
  newTab(\"Context\/Deposit\", true);
}"
replacement=""
perl -0777 -i.original -pe "s/\\Q$string/$replacement/igs" ui_schema.xml

# Remove duplicate dubtton from swipe menu
string="
  removeNavigationButton(\"duplicate\");"
replacement=""
perl -0777 -i.original -pe "s/\\Q$string/$replacement/igs" ui_logic.bsh
string="
  addNavigationButton(\"duplicate\", new ActionButtonCallback() {
    actionOnLabel() {
      \"{Duplicate}\";
    }
    actionOn() {
      if(!isNull(getUuid(tabgroup))) {
          duplicateRecord(tabgroup);
      } else {
          showWarning(\"{Warning}\", \"{This_record_is_unsaved_and_cannot_be_duplicated}\");
      }
    }
  }, \"primary\");"
replacement=""
perl -0777 -i.original -pe "s/\\Q$string/$replacement/igs" ui_logic.bsh

rm ui_logic.bsh.original
rm ui_schema.xml.original
