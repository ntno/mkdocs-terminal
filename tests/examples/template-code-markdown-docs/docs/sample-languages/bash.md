# Bash

Bash language highlighting with HIGHLIGHTING_METHOD_PLACEHOLDER:

```bash
#!/bin/bash
echo "Today is " `date`

echo -e "\nenter the path to a directory"
read the_path

echo -e "\nfiles and folders: "
ls $the_path
```

Script adapted from Zaira Hira's ["Bash Scripting Tutorial Linux Shell Script and Command Line For Beginners"](https://www.freecodecamp.org/news/bash-scripting-tutorial-linux-shell-script-and-command-line-for-beginners/)

## Inline Example

The ```:::bash printf``` and ```:::bash echo``` commands can be used to print text to the screen in a shell session.  However, `:::bash printf` supports text formatting and `:::bash echo` does not.

Read input interactively from the command line: ```:::bash read the_path```.