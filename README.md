# Temporary Object Library

A library for working with temporary items within the file system.

This means the allocation and destruction of a buffer or group of buffers will be managed
by this context.

## Types of Items

1. File: An individual buffer that may be written to. Upon completion of the program, the
   file should be assumed to be deleted and may not be referenced anymore.
1. Directory: The parent node of a group of files and directories. Just as before, all
   items in this directory should be assumed to be deleted after each run of the program.

[![asciicast](https://asciinema.org/a/OPfA1StKEo0imUxFnQqWWEB3G.svg)](https://asciinema.org/a/OPfA1StKEo0imUxFnQqWWEB3G)

