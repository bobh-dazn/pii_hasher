# pii_hasher
A python script which takes a CSV input and hashes any fields you specify to avoid sharing PII or confidential data.

# Usage
python3 hashme7.py <inputfile>.csv [--columns {names of columns}]

If you don't specify --columns then it will itterate through all the CSV columns and ask you what to hash.

The --columns argument is a space separated list of the names of the columns in the file.

The output will be a new file with the original filename and prefixed with "hashed_".
