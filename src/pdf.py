import re
import subprocess
from os import path
from urlparse import urlparse

from bs4 import BeautifulSoup
from flask import render_template
from flask import url_for

from src.grammar import get_grammar

root_folder_path = path.dirname(path.dirname(__file__))
pdf_folder_path = path.join(root_folder_path, 'pdf')

PDF_CONFIG = {
    'encoding': 'UTF-8',
    'page-size': 'A4',
    'margin-top': '1in',
    'margin-right': '0.7in',
    'margin-bottom': '0.8in',
    'margin-left': '0.7in',
    'print-media-type': '',
    'footer-center': '[page]',
    'footer-font-size': '9',
    'footer-spacing': '7',
    'enable-smart-shrinking': '',
    'zoom': '0.9'
}

PDF_TOC_CONFIG = {
    'xsl-style-sheet': path.join(pdf_folder_path, "toc.xsl")
}


def generate_pdf():
    output_file_path = path.join(pdf_folder_path, 'kotlin-docs.pdf')
    arguments = ["wkhtmltopdf"]
    for name, value in PDF_CONFIG.iteritems():
        arguments.append("--" + name)
        if value != '':
            arguments.append(value)
    arguments.append('cover')
    arguments.append(path.join(pdf_folder_path, 'book-cover.html'))
    arguments.append('toc')
    for name, value in PDF_TOC_CONFIG.iteritems():
        arguments.append("--" + name)
        arguments.append(value)
    arguments.append(url_for('pdf_content', _external=True))
    arguments.append(output_file_path)

    subprocess.check_call(arguments, cwd=pdf_folder_path, shell=True)
    return output_file_path



def get_pdf_content(pages, toc):
    """
    :type pages: flask.ext.flatpages.flatpages.FlatPages
    :param pages:
    """
    content = []
    for toc_section in toc:
        section = {
            'id': toc_section['title'].replace(' ', '_'),
            'title': toc_section['title'],
            'content': []
        }
        for reference in toc_section['items']:
            url = reference['url']
            if url.startswith('/'):
                url = url[1:]
            if url.endswith('.html'):
                url = url[:-5]

            if url == "docs/reference/grammar":
                page_html = render_template('pages/grammar.html', kotlinGrammar=get_grammar()).replace("<br>", "<br/>")
                document = BeautifulSoup(page_html, 'html.parser')
                document = document.find("div", {"class": "grammar"})
                page_id = "grammar"
                title = "Grammar"
            else:
                page = pages.get(url)
                if page is None:
                    continue
                title = page.meta['title']
                document = BeautifulSoup(page.html, 'html.parser')
                page_id = page.path.split('/')[-1]

            for element in document.find_all():
                if 'id' in element.attrs:
                    element.attrs['id'] = page_id + '_' + element.attrs['id']
                if element.name == "a":
                    if 'href' not in element.attrs:
                        continue
                    href = element.attrs['href']
                    url = urlparse(href)
                    if url.scheme == "":
                        if href.startswith('#'):
                            new_href = page_id + '_' + href[1:]
                        else:
                            url_path = url.path[:-5] if url.path.endswith(".html") else url.path
                            new_href = url_path + ('_' + url.fragment if url.fragment != "" else "")
                        element.attrs['href'] = "#" + new_href

                header_regex = re.compile('^h(\d)$')
                if header_regex.match(element.name):
                    level = int(header_regex.match(element.name).group(1)) + 1
                    element.name = 'h' + str(level)

            section['content'].append({
                'id': page_id,
                'title': title,
                'content': document.decode()
            })
        content.append(section)
    page_html = render_template('pdf.html', content=content, static_folder=path.join(path.dirname(__file__), "static"))
    return page_html
