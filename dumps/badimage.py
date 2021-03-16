#!/usr/bin/python

import mmap
import PIL.Image as PILImage

with open("/home/npgentry/games/cxt/garage/data/100.cxt") as f:
    stream = mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ)
    stream.seek(0x4ba14)
    raw = stream.read(0x4e3a2 - stream.tell())
    image = PILImage.frombytes("P", (248, 42), data=raw)
    image.save("../graphics/bad.png")
