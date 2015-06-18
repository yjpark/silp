0.3.1
-----
Add simple plugin support for more complex macro.

- Currently plugins should be put under project's silp_plugins
    (Project means the folder holding silp_xx.md)
- plugin macro has format as module:func(param1, param2, ...)
    module here is the name of the python plugin, func is the name of
    function
- also expose silp.error/info/verbose, then the plugin codes can print
    debug information with them.

Add support for Erlang (both erl, and hrl)

0.2.5
-----
Add support for YML launguage

0.2.4
-----
Fix the wrong `import silp` in setup.py which breaks the dependencies installation.

- https://github.com/yjpark/silp/issues/1
- Thanks for lowks for the comment: https://github.com/lowks

0.2.3
-----

### --clean
Add `--clean` parameter to remove silp generated lines, usefel if want
  to change the language settings

### include other files in template
The syntax is something like:
```
<<[fish/fish.freshrc]
```
This is following the Marked (a markdown preview app on OS X) rule, so Marked
can show the included file content just fine.

### freshrc support
freshshell is a very nice tool to manage dotfiles, though it doesn't support
include other freshrc at the moment(2014-05-06), so I split my freshrc into
smaller files, and use silp to put them into the main file.
- https://github.com/freshshell/fresh

0.2.2
-----
- Bugfix with the .md files not included in Manifest

0.2.1
-----
- Change name to "Simple Individual Line Preprocessor"

0.2.0
-----
- Better control with the padding spaces to keep all `generated_surfix` aligned
- Skipping files that not using SILP, to prevent the useless files in `.silp_backup`
  and `.silp_test` folders
- Can support multiple project setting files with different extentions
- If a subfolder has it's own setting files, won't include them in the parant's `--all` run

0.1.0
-----
First version, can do basic processing
