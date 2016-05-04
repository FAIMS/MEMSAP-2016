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
  newTab(\"Context\/Context_Deposits\", true);
}"
replacement=""
perl -0777 -i.original -pe "s/\\Q$string/$replacement/igs" ui_logic.bsh

# Link Start_Depth_Magnitude to data schema as measure
string="<input ref=\"Start_Depth_Magnitude\""
replacement="$string faims_attribute_type=\"measure\""
perl -0777 -i.original -pe "s/\\Q$string/$replacement/igs" ui_schema.xml

# Delete autogenerated onClickContextUpdateTexture definition.
string="
onClickContextUpdateTexture () {
  \/\/ TODO: Add some things which should happen when this element is clicked
  newTab(\"Context\/Context_Deposits\", true);
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
