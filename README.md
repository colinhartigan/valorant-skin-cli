## NOTE: This does not grant free skins; it only works with skins you already own.

![header](https://user-images.githubusercontent.com/42125428/124552512-a8027900-de01-11eb-9e85-b19f82d2eee6.png)

> A simple command line interface to manage VALORANT skins, including a skin randomizer

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub License](https://img.shields.io/github/license/colinhartigan/valorant-skin-cli)](https://github.com/colinhartigan/valorant-skin-cli/blob/master/LICENSE)
[![Discord](https://img.shields.io/badge/discord-join-7389D8?style=flat&logo=discord)](https://discord.gg/uGuswsZwAT)
[![GitHub issues](https://img.shields.io/github/issues/colinhartigan/valorant-skin-cli)](https://github.com/colinhartigan/valorant-skin-cli/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/colinhartigan/valorant-skin-cli)](https://github.com/colinhartigan/valorant-skin-cli/pulls)
![GitHub Repo stars](https://img.shields.io/github/stars/colinhartigan/valorant-skin-cli?style=social)
[![BetterREADME Verified](https://img.shields.io/badge/BetterREADME-Verified-grey?logo=github&labelColor=white&logoColor=grey)](https://github.com/better-readme)


### Table of Contents
1. [Demo](#demo)
2. [Getting Started](#getting-started)
3. [Current Features](#current-features)
4. [FAQ](#faq)
5. [What's next](#whats-next)
6. [Contribute](#contribute)
7. [Dependencies](#dependencies)
8. [Legal](#legal)

<br/>

## Demo
https://user-images.githubusercontent.com/29008608/124373643-37067880-dcbe-11eb-8cea-724e6150978f.mp4

<br/>

## Getting Started
### Setup

**Download the `.exe` file from the [latest release](https://github.com/colinhartigan/valorant-skin-cli/releases/latest)**

> __NOTE__: Your antivirus might mark the executable as malware, but this is a side effect of building the executable with PyInstaller. Check [FAQ](#faq) for further information and steps to get back your file.
> _I've rebuilt the executables with Python 3.7 and it seems they aren't being marked as malware anymore!_

If you'd rather build the executable yourself, download the release `.zip` file and run `build.bat`, or `run.bat` to execute the script directly. To test the latest features, clone the repository.

### Usage
1. Ensure that VALORANT is already running. This app requires VALORANT to be running
2. Run the `.exe` file you downloaded

This presents you with a command line interface(CLI) where you need to type in commands to navigate the program. Basic setup of the program can he found [here](https://github.com/colinhartigan/valorant-skin-cli/wiki/Setup) and the full list of commands are available [here.](https://github.com/colinhartigan/valorant-skin-cli/wiki/Commands)

<br/>

## Current Features
* Randomise skins with full customisation of what gets randomised
* Change individual skin levels and chromas. This includes downgrading skins which is not possible in-game
* Loadout system with multiple loadouts

<br/>

## FAQ
**Q: Will I get banned for using this?**  
A: [u/Riot_Giraffy (Riot Employee) confirmed:](https://www.reddit.com/r/VALORANT/comments/oae5g6/i_got_tired_of_waiting_for_riot_to_add_a_skin/h3hwxtf?utm_source=share&utm_medium=web2x&context=3)
> Using the client API to modify loadouts does not seem ban worthy. The client API isn't officially supported for third party use, so don't expect future compatibility.


**Q: How do I downgrade my skins?**  
A: For example, if you want to set your Prime Karambit to Level 1: `set Melee Prime//2.0-Karambit Level-1`  


**Q: Can I set the skin to something I don't own?**  
A: No.


**Q: Why does windows defender say it's a virus?**
A: [@markhank:](https://medium.com/@markhank/how-to-stop-your-python-programs-being-seen-as-malware-bfd7eb407a7)
>Code compiled using pyinstaller or py2exe is often incorrectly to be malware or a virus or a trojan by various antivirus programs. It can often have scary names like Trojan:Win32/Wacatac.C!ml.
This is most likely what is known in the virus industry as a “false positive”. Your code might not be doing anything malicious, but because it was compiled in a way that looks a bit like other code which might do malicious things antivirus judges it to be a virus.

To recover the `.exe` from Windows Defender:
1. Open Windows Defender
2. Select  **Virus & threat protection**  and then click  **Protection history**
3. In the list of all recent items, filter on  **Quarantined Items**
4. Select the `.exe`, press the **Actions** button, and press Restore

To prevent Windows Defender from quarantining the file again:
1. Open Windows Defender
2. Select  **Virus & threat protection**  and under  **Virus & threat protection setting** click **Manage settings**
3. Scroll down to **Exclusions** and click **Add or remove exclusions**
4. Click **Add an exclusion**, click **File** and then select the downloaded`.exe`file

<br/>

## What's next
- [X] Loadout profile system
-  - [ ] Loadout profile randomizer
- [ ] Spray randomizer 
- [ ] Gun buddy randomizer

<br/>

## Contribute
Have an idea or a suggestion? Drop an issue or create a pull request!

<br/>

## Dependencies
Check [requirements.txt](https://github.com/colinhartigan/valorant-skin-cli/blob/master/requirements.txt) for updated infomation!
```
valclient
requests
InquirerPy
PyInstaller
```

<br/>

## Legal
This project is not affiliated with Riot Games or any of its employees and therefore does not reflect the views of said parties. This is purely a fan-made project to enhance VALORANT's skin inventory management.

Riot Games does not endorse or sponsor this project. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc. 
