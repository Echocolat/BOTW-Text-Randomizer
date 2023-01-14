## BOTW Text Randomizer v1 by Echocolat

#### What is it ?

BOTW Text Randomizer is a script that can shuffle all of the text in the game. This allows a fun experience, for example when re creating a save file for a bigger mod. (you just have to put the Text Rando mod over in terms of priority) You also are able to choose whether or not you want to randomize certain types of texts, randomize only texts in a certain category (like, all of the actor texts only can be replaced with another actor text), and even take a modded textfile to use the text randomizer on custom texts too.

#### How to use it ? 

First, you have to edit the `config.json` file. Here's what the different parameters do :  
- `name_of_pack` : Is basicallky `Bootup_[Lang].pack` where Lang is RegionLanguage.  
- `use_mod_file` : `true` if you want to apply the text rando on a modded text file. Has to be used with `file_path_only_for_mod_file`.  
- `file_path_only_for_mod_file` : Relative path to your modified text file. Don't forget to double slash between repos.  
- `randomize_[type]_text` : Whether or not the `type` of text is randomized. Ignored if `randomize_all` is set to true.  
- `randomize_all` : If set to true, the text rando will change text regardless of their type. If set to false, it will only randomize the type of text referenced in the `randomize_[type]_text`, and only a text from a certain type will be able to change a text from the same type. (for example, an actor text can only be replaced with another actor text)  

Then, just launch `main.py`. After it finishes, install `Text Randomizer\\rules.txt` with BCML, and enjoy! :)

#### If it doesn't work : 

Verify you have all of the packages installed, even though you should have them if you're using BCML. The packages are `oead`, `bcml`, `pymsyt`, `json`, `os` and `random`. Type `pip install [package]` where `[package]` is the package you want to install in a terminal or a cmd. If it still doesn't work, check that your modded text file (if you're using the option) path is correctly set. Finally, if it still doesn't work, consider contacting me through Discord (Echocolat#9988).  