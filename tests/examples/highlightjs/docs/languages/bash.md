# Bash

Here's a sample bash script:

```bash
#!/bin/bash
echo "Today is " `date`

echo -e "\nenter the path to a directory"
read the_path

echo -e "\nthis path has the following files and folders: "
ls $the_path
```

Script adapted from Zaira Hira's ["Bash Scripting Tutorial Linux Shell Script and Command Line For Beginners"](https://www.freecodecamp.org/news/bash-scripting-tutorial-linux-shell-script-and-command-line-for-beginners/)