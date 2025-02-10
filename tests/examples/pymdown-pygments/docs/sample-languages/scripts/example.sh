#!/bin/bash
echo "Today is " $(date)

echo -e "\nenter the path to a directory"
read the_path

echo -e "\nfiles and folders: "
ls $the_path