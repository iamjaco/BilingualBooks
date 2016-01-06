import ebooklib
from ebooklib import epub
import epub
import itertools
from BeautifulSoup import BeautifulSoup, Tag

INVERT = False
book1 = epub.read_epub('data/swedish.epub')
book2 = epub.read_epub('data/english1.epub')
book3 = epub.EpubBook()


book3 = epub.EpubBook()
book3.metadata = book1.metadata

for item in list(book1.get_items()):
    if item.get_type() == ebooklib.ITEM_IMAGE:
        print 'image'
        item.file_name = item.file_name.replace('OEBPS/', '')
        print item.file_name
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        print item
        continue
    book3.add_item(item)

for item in list(book2.get_items()):
    if item.get_type() == ebooklib.ITEM_IMAGE:
        print 'image'
        item.file_name = item.file_name.replace('OEBPS/', '')
        print item.file_name
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        print item
        continue
    book3.add_item(item)

doc_list1 = list(book1.get_items_of_type(ebooklib.ITEM_DOCUMENT))
doc_list2 = list(book2.get_items_of_type(ebooklib.ITEM_DOCUMENT))

doc_list1.remove(book1.get_item_with_id(book1.spine[1][0]))
doc_list2.remove(book2.get_item_with_id(book2.spine[0][0]))
doc_list2.remove(book2.get_item_with_id(book2.spine[-1][0]))

book2.spine = book2.spine[1:-1]
del book1.spine[1]

for i in range(len(book1.spine)):
    if book1.get_item_with_id(book1.spine[i][0]) not in doc_list1:
        continue
    #print doc_list2[i].get_body_content()[:100]
    doc1_index = doc_list1.index(book1.get_item_with_id(book1.spine[i][0]))
    doc2_index = doc_list2.index(book2.get_item_with_id(book2.spine[i][0]))

    soup1 = BeautifulSoup(doc_list1[doc1_index].content)
    soup2 = BeautifulSoup(doc_list2[doc2_index].content)

    pars1 = soup1.findAll('p')
    pars2 = soup2.findAll('p')

    try:
        print soup2.head.findAll('link')[0]['href']
        print len(pars1)
        print len(pars2)
        mixed_pars = list(itertools.chain.from_iterable(itertools.izip_longest(pars1, pars2)))
        mixed_pars = [par for par in mixed_pars if par is not None]
        print len(mixed_pars)

        for p in soup1.findAll('p'):
            p.extract()
        for p in mixed_pars:
            soup1.body.insert(mixed_pars.index(p), p)
        css_el = soup2.head.findAll('link')[0]
        css_el['href'] = 'OEBPS/' + css_el['href']
        soup1.head.insert(0, css_el)
        doc_list1[doc1_index].content = soup1.prettify()
    except:
        print 'except'
        continue

    # print doc_list2[i].content[:400]
    # print type(doc_list2[i].content[:400])

for item in doc_list1:
    book3.add_item(item)
# print book1.spine
# print
# print book2.spine
print len(book1.spine)
print len(book2.spine)


# basic spine
if not INVERT:
    book3.spine = list(itertools.chain.from_iterable(zip(book1.spine,book2.spine)))
else:
    book3.spine = list(itertools.chain.from_iterable(zip(book2.spine,book1.spine)))

epub.write_epub('The Girl With The Dragon Tatoo EN-SV(Mixed paragraphs).epub', book3, {})
