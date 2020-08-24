# Key Database Manager

This is a tool developed to help build and maintain a database intended to be used by the **Not a Key** project. Not a Key is an identification tool, similar to a dichotomous key, but *dynamic*. This tool is being developed to aid with mosquito (Diptera: Culicidae) identification by non-specialists.

There exists both a GUI Application made with PyQt5 and a Terminal Application made using the python curses module. Both do the same thing: provide a user friendly environment to manually update the `key_database` that is queried by the Not a Key project.

For use, the applications (both GUI and TA) require the modification of the configuration file `conf` to add the User, Host and Password for the MySQL server hosting the `key_database`. Both also utilize the files `SPECIES.txt` and `COUPLETS.txt`, in the 'select' folder, to show to the user only select species/couplets, as opposed to the whole database. This means that the database admin must provide lists with the correct names of couplets and species that exist in the database tables. The current files in this repository contain all the mosquito (Diptera: Culicidae) species in the U.S.A., and all the couplets currently in use for mosquito identification in the Not a Key project (this is an unfinished list).

The Terminal Application also accepts custom configuration for its key bindings, check the `conf` file for more information.
