<h1 align="center">Valorant skin manager CLI</h1>

> Simple command line interface to manage Valorant skins with a skin randomizer

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub License](https://img.shields.io/github/license/colinhartigan/valorant-skin-cli)](https://github.com/colinhartigan/valorant-skin-cli/blob/master/LICENSE)
[![Discord](https://img.shields.io/badge/discord-join-7389D8?style=flat&logo=discord)](https://discord.gg/uGuswsZwAT)
[![GitHub issues](https://img.shields.io/github/issues/colinhartigan/valorant-skin-cli)](https://github.com/colinhartigan/valorant-skin-cli/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/colinhartigan/valorant-skin-cli)](https://github.com/colinhartigan/valorant-skin-cli/pulls)
![GitHub Repo stars](https://img.shields.io/github/stars/colinhartigan/valorant-skin-cli?style=social)
[![BetterREADME Verified](https://img.shields.io/badge/BetterREADME-Verified-grey?logo=github&labelColor=white&logoColor=grey)](https://github.com/better-readme)


### Table of Contents
1. [Demo](#demo)
2. [Installation and usage](#installation-and-usage)
3. [FAQ: Ban or no ban?](#am-i-getting-banned)
4. [TODOs](#todos)
5. [Dependencies](#dependencies)
6. [Contribute](#contribute)


## Demo
https://user-images.githubusercontent.com/42125428/124053877-05a45900-d9ef-11eb-9acc-fb71edfcc487.mp4


## Installation and usage
### Installation
Clone the repo, or simply download the `.zip` file.

Install [__Python 3.9__](https://www.python.org/downloads/release/python-377/) and open the command line in the repo folder

```shell
python3 -m pip install -r requirements.txt
python3 main.py
```

Note: Using `python3` on Windows 8/10 may open the Store, in that case use `python`

### Usage
The following commands are available for usage

- `randomize` - Randomizes your skins manually (will still automatically happen after each match)
- `modify` - Modify which skins enabled for randomization (use arrow keys and enter to select)
- `set <gun> <skin>` - Manually set a skin, eg. `set Phantom Oni Phantom`
- `exit` - Self explanatory


## Am I Getting Banned
Riot Dev confirmed:
> Using the client API to modify loadouts does not seem ban worthy. The client API isn't officially supported for third party use, so don't expect future compatibility.


## TODOs
- [x] [Onboarding Experience](https://github.com/colinhartigan/valorant-skin-cli/commit/79739958c8bc632a2e8ec91f533c4fe2fba607dd#diff-bd516d79afd4ace3e4372b8ccab756b47b74da5ac479f373258ddcb3c4159ff2)
- [x] [Configuraion Command](https://github.com/colinhartigan/valorant-skin-cli/commit/973dee78becbfbda1c6f3cfd9f7e929f823ae8ec#diff-77765503b3f273fa49a93e1c5bfa59786213a26f2143d7a6ad75fbd2c38d5cd2)
  - Set refresh interval 
  - Set region
  - ~~Reset/Regen skin inventory~~ (coming in a future update after v1)
- [ ] Documentations


## Dependencies
Better check [requirements.txt](https://github.com/colinhartigan/valorant-skin-cli/blob/master/requirements.txt) for updated infomation

```
valclient
requests
termcolor
InquirerPy
```

## Contribute
Do what you can to help the project. Issues and pull requests are welcome.

