# passpls
## Passwords Please! - A companion for generating passwords for password spraying
passpls will create an extensive list of passwords, based on specified modifiers, that can be used for password spraying. **This tool is not meant to be an all encompassing password generator.** It is simply made to quickly spit out some of the most popular passwords to test.

### Usage 
Note: Modifier "w" ensures the password meets AD password complexity, which means the password has to have at least three of the following (excluding unicode):
- Lowercase
- Uppercase
- Special character
- Number
```
$ ./passpls.py -h
usage: passpls.py [-h] [-i INPUT] [-o OUTPUT] [-m x [x ...]] [-d x [x ...]]

Passwords Please! - A companion for generating passwords for password spraying. (https://github.com/e-nzym3/passpls)

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        (Optional) File containing a list of passwords to be modified. If not specified, will generate a default list using months (-d m), common passwords (-d c), and seasons (-d s).
  -o OUTPUT, --output OUTPUT
                        (Optional) File to which the modified passwords will be written. If not specified, will write to '[local directory]/modified_passwords.txt'.
  -m x [x ...], --modifiers x [x ...]
                        (Optional) Modifiers to be used while processing the input file. (Defaults to 't l y r'.) 
                            Example: '-m t y w'
                        * Available modifiers are: 
                          t (title), 
                          l (lowercase), 
                          u (uppercase), 
                          y (years), 
                          r (common trailers), 
                          w (Windows/AD Compliant).
  -d x [x ...], --defaults x [x ...]
                        (Optional) Use pre-defined default/common passwords during processing. 
                            Example: '-d s m c' 
                        * Available lists for these include:
                          s (seasons), 
                          d (days of the week), 
                          c (common/default passwords), 
                          e (extended common/default passwords), 
                          m (months of the year).
```

### Example
input_list.txt:
```
Github
lakers
DISNEY
```
Command: 
```./passpls -i input_list.txt -o output_list.txt -m t y r w -d s```

Output:
```
$ cat output_list.txt
DISNEY123!
DISNEY123#
DISNEY123$
DISNEY2022!
DISNEY2022#
DISNEY2022$
DISNEY2022@
DISNEY2023!
DISNEY2023#
DISNEY2023$
DISNEY2023@
Disney!
Disney#
Disney$
Disney.
Disney123
Disney123!
Disney123#
Disney123$
Disney1234
Disney2022
Disney2022!
Disney2022#
Disney2022$
Disney2022@
Disney2023
Disney2023!
Disney2023#
Disney2023$
Disney2023@
Disney22
Disney23
Disney?
Disney@
Github!
Github#
Github$
Github.
Github123
Github123!
Github123#
Github123$
Github1234
Github2022
Github2022!
Github2022#
Github2022$
Github2022@
Github2023
Github2023!
Github2023#
Github2023$
Github2023@
Github22
Github23
Github?
Github@
Lakers!
Lakers#
Lakers$
Lakers.
Lakers123
Lakers123!
Lakers123#
Lakers123$
Lakers1234
Lakers2022
Lakers2022!
Lakers2022#
Lakers2022$
Lakers2022@
Lakers2023
Lakers2023!
Lakers2023#
Lakers2023$
Lakers2023@
Lakers22
Lakers23
Lakers?
Lakers@
lakers123!
lakers123#
lakers123$
lakers2022!
lakers2022#
lakers2022$
lakers2022@
lakers2023!
lakers2023#
lakers2023$
lakers2023@
```
