import os
import re

path = "."
for root, unused_dirs, files in os.walk(path):
   for f in files:
     if f.endswith(".txt"):
         with open(f) as fr:
           lines = fr.readlines()
         with open(f,"w") as fw:
           for line in lines:
             line = re.sub(r"\r\r","\n",line.strip())
             fw.write(re.sub(r"\r","\n",line.strip()))
