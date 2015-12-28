#!/usr/bin/env python

from gi.repository import Gtk
import urllib
import sys

class LeetSpeak():
    def __init__(self):
        self.x = '1337'

    def toLeet(self, text):
        leet = (
            (('are', 'Are'), 'r'),
            (('ate', 'Ate'), '8'),
            (('that', 'That'), 'tht'),
            (('you', 'You'), 'j00'),
            (('o', 'O'), '0'),
            (('i', 'I'), '1'),
            (('e', 'E'), '3'),
            (('s', 'S'), '5'),
            (('a', 'A'), '4'),
            (('t', 'T'), '7'),
            )
        for symbols, replaceStr in leet:
            for symbol in symbols:
                text = text.replace(symbol, replaceStr)
        return text

class ESVSession:
    def __init__(self, key):
        options = ['include-short-copyright=0',
                   'output-format=plain-text',
                   'include-passage-horizontal-lines=0',
                   'include-heading-horizontal-lines=0',
                   'include-headings=0',
                   'include-footnote-links=0',
                   'include-footnotes=0',
                   'include-passage-references=0',
                   'include-first-verse-numbers=0']
        self.options = '&'.join(options)
        self.baseUrl = 'http://www.esvapi.org/v2/rest/passageQuery?key=%s' % (key)

    def doPassageQuery(self, passage):
        passage = passage.split()
        passage = '+'.join(passage)
        url = self.baseUrl + '&passage=%s&%s' % (passage, self.options)
        page = urllib.urlopen(url)
        return page.read()

class ESVtoLeetGTK:

    def __init__(self):
        self.gladefile = "esvtoleet_gtk.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")

        self.style_context = self.window.get_style_context()

        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_path('esvtoleet.css')

        self.style_context.add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.window.show_all()

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, ok_button):
        self.raw_text = self.builder.get_object("raw_text")
        self.leet_text = self.builder.get_object("leet_text")

        self.passage_input = self.builder.get_object("passage_input")
        self.passage = str(self.passage_input.get_text())
        self.passage_text = bible.doPassageQuery(self.passage)

        self.passage_leet = ' '

        if self.passage_text != 'ERROR: No passage found for your query.':
            self.passage_leet = leet.toLeet(self.passage_text)

        self.leet_text.set_text(self.passage_leet)
        self.raw_text.set_text(self.passage_text)


if __name__ == "__main__":
    key = 'IP'
    bible = ESVSession(key)
    leet = LeetSpeak()
    main = ESVtoLeetGTK()
    Gtk.main()

