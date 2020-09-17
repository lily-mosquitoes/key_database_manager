# Key Database Manager

![tests](https://github.com/lily-mosquitoes/key_database_manager/workflows/tests/badge.svg)
[![release](https://img.shields.io/github/v/release/lily-mosquitoes/key_database_manager?include_prereleases)](https://github.com/lily-mosquitoes/key_database_manager/releases)

Key Database Manager is a tool developed to help build and maintain a the `key_database`, a database intended to be used with the **Not a Key** project. Not a Key is an identification tool, similar to a dichotomous key, but *dynamic*. This tool is being developed to aid with mosquito (Diptera: Culicidae) identification by non-specialists.

There exists both a GUI Application made with Qt and a Terminal Application made using the python curses module. Both do the same thing: provide a user friendly environment to manually update the `key_database` that is queried by the Not a Key project.

For use, the applications (both GUI and TA) require the input of the User, Host and Password for the MySQL server hosting the `key_database`, the input is given from within the applications and stored in a `.config` file under the 'config' folder for subsequent runs; it is important to note that for now the password is stored in plain text, this could be changed with the use of the `keychain` module in the future. Both also utilize the filter files from the 'select' folder, `SPECIES.txt` and `COUPLETS.txt`, to show to the user only select species/couplets, as opposed to the whole data of the database. This means that the database admin must provide lists with the correct names of couplets and species that exist in the database tables. The current files in this repository contain all the mosquito (Diptera: Culicidae) species in the U.S.A., and all the couplets currently in use for mosquito identification in the Not a Key project (this is an unfinished list).

The Terminal Application also accepts custom configuration for its key bindings, which you can set at runtime.

## Features:

An 'actions' menu was introduced, there you can change your current password (the `.config` file will be automatically updated accordingly) and perform bulk updates of characters.

For bulk updates a `.csv` file must be provided, with the following configuration:

|  | Unique Species Name A | Unique Species Name B | Unique Species Name C |
|-|-|-|-|
| Unique Couplet Name 1 | 0 | 1 | 01 |
| Unique Couplet Name 2 | 10 | NA | NULL |

**Accepted values are: 0, 1, 01, 10, NA and NULL**

\t *Attention: if typing 01 in a spreadsheet software, make sure it does not turn into a 1 (due to automatic number formatting); alternatively, you may type 10 instead, as the Not-a-Key program will not differentiate between the two formats.*

## How to get it:

Click on [releases](https://github.com/lily-mosquitoes/key_database_manager/releases) and you will find a set of `.zip` files under 'assets'. Download the `.zip` file corresponding to your system, unzip it and run the executable from either the GUI Application (under the folder `key_database_manager`) or the Terminal Application (under the folder `ta_key_database_manager`)

## Running it from source:

Install the requirements:
`python3 -m pip install -r requirements.txt`

To run the GUI Application:
`python3 key_database_manager.py`

To run the Terminal Application:
`python3 ta_key_database_manager.py`
