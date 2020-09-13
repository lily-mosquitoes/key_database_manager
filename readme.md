# Key Database Manager

![release](https://img.shields.io/github/v/release/lily-mosquitoes/key_database_manager?include_prereleases)

This is a tool developed to help build and maintain a database intended to be used by the **Not a Key** project. Not a Key is an identification tool, similar to a dichotomous key, but *dynamic*. This tool is being developed to aid with mosquito (Diptera: Culicidae) identification by non-specialists.

There exists both a GUI Application made with Qt and a Terminal Application made using the python curses module. Both do the same thing: provide a user friendly environment to manually update the `key_database` that is queried by the Not a Key project.

For use, the applications (both GUI and TA) require the input of the User, Host and Password for the MySQL server hosting the `key_database`, the input is given from within the applications and stored in a `.config` file under the 'config' folder for subsequent runs; it is important to note that for now the password is stored in plain text, this could be changed with the use of the `keychain` module in the future. Both also utilize the filter files from the 'select' folder, `SPECIES.txt` and `COUPLETS.txt`, to show to the user only select species/couplets, as opposed to the whole data of the database. This means that the database admin must provide lists with the correct names of couplets and species that exist in the database tables. The current files in this repository contain all the mosquito (Diptera: Culicidae) species in the U.S.A., and all the couplets currently in use for mosquito identification in the Not a Key project (this is an unfinished list).

The Terminal Application also accepts custom configuration for its key bindings, which you can set at runtime.

## Changes:

The applications were changed to set up the `.config` file at runtime, you may change the configurations from within the applications at any time; if you must completely reset configurations simply delete the file; do not manually change it.

The key bindings stored in the `.config` file for the TA were changed to non-human-readable format (key codes from the python `ord()` function). This was done to simplify coding, since the file isn't supposed to be manually edited anymore.

## Running it:

Install the requirements:
`python3 -m pip install -r requirements.txt`

To run the GUI Application:
`python3 key_database_manager.py`

To run the Terminal Application:
`python3 ta_key_database_manager.py`
