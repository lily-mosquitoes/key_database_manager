# Key Database Manager

![tests](https://github.com/lily-mosquitoes/key_database_manager/workflows/tests/badge.svg)
[![release](https://img.shields.io/github/v/release/lily-mosquitoes/key_database_manager?include_prereleases)](https://github.com/lily-mosquitoes/key_database_manager/releases)

Key Database Manager is a tool developed to help build and maintain a database of character states (dubbed the *key database*) intended to be used with the **Not a Key** project. Not a Key is an identification tool, similar to a dichotomous key, but *dynamic*. This tool is being developed to aid with mosquito (Diptera: Culicidae) identification by non-specialists.

There exists both a GUI Application made with Qt and a Terminal Application made using the python curses module. Both do the same thing: provide a user friendly environment to manually update the *key database*, which will be queried by the Not a Key project.

The applications use PyMySQL to connect to the *key database*. All credentials are given at runtime and stored in a `.config` file under the 'config' folder for subsequent runs; it is important to note that, for now, the password is stored in plain text, this could be changed with the use of the `keychain` module, or a similar module, in the future.

## Usage:

Both the GUI Application and the Terminal application serve the same purpose, to update character states for each species regarding each couplet present in the database.

You must provide login credentials to access the database of character states you want to update. The fields you must provide are: user, host, password and database.

Additionally, you must provide filter files for couplets and species present in the database you want to update. The files must be `.txt` files, which are lists of names, each in a newline. This is supposed to make it easier to update small portions of the database at any given time, as you won't need to scroll through tons of couplets/species to update the ones you want. However it creates two inconveniences: the database admin must provide lists of correct names of couplets and species for users to build your filter files, and they must update users on changed couplet/species names; and you must change the filter files to match the database you want to access at login time. This may be removed in the future if the advantages don't outweigh the disadvantages, otherwise it also may be changed to a more robust system of filtering from within the application.

## Features:

**Multiple logins:** in the login screen you can add new login information or change your currently selected login information. This allows for access to multiple databases with the same user, as well as multiple user access in the same device.

**Password change:** in the 'actions' menu, you may change your database access password, this will affect the database user credentials directly and it will subsequently update your configuration files. New passwords must be at least 8 characters long; you will be prompted to type your new password twice to avoid typing errors.

**Bulk updates:** in the 'actions' menu, you can perform bulk updates of characters using a `.csv` file. The provided `.csv` file must be in the following configuration:

|  | Unique Species Name A | Unique Species Name B | Unique Species Name C |
|-|-|-|-|
| Unique Couplet Name 1 | 0 | 1 | 01 |
| Unique Couplet Name 2 | 10 | NA | NULL |

**Accepted values are: 0, 1, 01, 10, NA and NULL**

* *Attention: if typing 01 in a spreadsheet software, make sure it does not turn into a 1 (due to automatic number formatting); alternatively, you may type 10 instead, as the Not-a-Key program will not differentiate between the two formats.*

## How to get it:

Click on [releases](https://github.com/lily-mosquitoes/key_database_manager/releases) and you will find a set of compressed files (`.zip` and `.tar.xz`) under 'assets'. Download the compressed file corresponding to your system (`Linux.tar.xz`, `macOS.tar.xz` or `Windows.zip`), uncompress it and run the executable for either the GUI Application (under the folder `key_database_manager`) or the Terminal Application (under the folder `ta_key_database_manager`)

## Running it from source:

Install the requirements:
`python3 -m pip install -r requirements.txt`

To run the GUI Application:
`python3 key_database_manager.py`

To run the Terminal Application:
`python3 ta_key_database_manager.py`

## Acknowledgments

Special thanks to Lyric Bartholomay, Chris Stone, Andrew Mackay and Corrado for supporting the project, and to Andrew Mackay and Corrado for testing the previous release and providing feedback.

Thanks to the [Midwest Center of Excellence for Vector-Borne Disease](http://mcevbd.wisc.edu/about) for providing financial support for the Not a Key project.
