import ebooklib
from ebooklib import epub
import epub
import itertools

INVERT = True
book1 = epub.read_epub('data/swedish.epub')
book2 = epub.read_epub('data/english1.epub')
book3 = epub.EpubBook()


book3 = epub.EpubBook()
book3.metadata = book1.metadata

for item in list(book1.get_items()):
    book3.add_item(item)

for item in list(book2.get_items()):
    book3.add_item(item)

book2.spine = book2.spine[1:-1]
del book1.spine[1]
print book1.spine
print
print book2.spine
print len(book1.spine)
print len(book2.spine)


# basic spine
if not INVERT:
    book3.spine = list(itertools.chain.from_iterable(zip(book1.spine,book2.spine)))
else:
    book3.spine = list(itertools.chain.from_iterable(zip(book2.spine,book1.spine)))

epub.write_epub('The Girl With The Dragon Tatoo EN-SV(Mixed chapters).epub', book3, {})
