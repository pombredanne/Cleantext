from unittest import TestCase

from cleantext import CleanText
from cleantext import ALLOWED_TAGS
from cleantext import ALLOWED_ATTRIBUTES


cleantext = CleanText(
    tags=ALLOWED_TAGS,
    attributes=ALLOWED_ATTRIBUTES,
    replace={
       'signature-texte': ('span', {}),
       'signature': ('b', {'class': 'signature'}),
    },
    delete=['note-technique'],
)



class MethodeCleantextTests(TestCase):

    def _test_keep_tag(self, tag):
        xml = '<%s>SPAM and EGG</%s>' % (tag, tag)
        output = cleantext(xml)
        expected = '<%s>SPAM and EGG</%s>' % (tag, tag)
        self.assertEqual(expected, output)

    def _test_keep_tag_and_clean_attributes(self, tag):
        xml = '<%s spam="spam" egg="egg">SPAM and EGG</%s>' % (
            tag,
            tag,
        )
        output = cleantext(xml)
        expected = '<%s>SPAM and EGG</%s>' % (tag, tag)
        self.assertEqual(expected, output)

    def test_keep_b(self):
        self._test_keep_tag('b')

    def test_keep_i(self):
        self._test_keep_tag('i')

    def test_keep_p(self):
        self._test_keep_tag('p')

    def test_keep_sub(self):
        self._test_keep_tag('sub')

    def test_keep_sup(self):
        self._test_keep_tag('sup')

    # Keep b, i, p, sub, sup but clear attributes

    def test_keep_b_and_clean_attributes(self):
        self._test_keep_tag_and_clean_attributes('b')

    def test_keep_i_and_clean_attributes(self):
        self._test_keep_tag_and_clean_attributes('i')

    def test_keep_p_and_clean_attributes(self):
        self._test_keep_tag_and_clean_attributes('p')

    def test_keep_sub_and_clean_attributes(self):
        self._test_keep_tag_and_clean_attributes('sub')

    def test_keep_sup_and_clean_attributes(self):
        self._test_keep_tag_and_clean_attributes('sup')

    # keep a

    def test_keep_a(self):
        xml = '<a>SPAM and EGG</a>'
        output = cleantext(xml)
        expected = '<a>SPAM and EGG</a>'
        self.assertEqual(expected, output)

    def test_keep_a_and_do_not_clean_attributes(self):
        xml = '<a href="www.example.tld" foo="foo" bar="bar">SPAM and EGG</a>'
        output = cleantext(xml)
        expected = '<a href="www.example.tld">SPAM and EGG</a>'
        self.assertEqual(expected, output)

    def test_delete_notetechnique(self):
        xml = '<note-technique>SPAM and EGG</note-technique>'
        output = cleantext(xml)
        expected = ''
        self.assertEqual(expected, output)

    # Replace

    def _test_replace_with_class(self, tag, new_tag, new_class):
        xml = '<%s spam="spam" egg="egg">SPAM and EGG</%s>' % (
            tag,
            tag,
        )
        output = cleantext(xml)
        if new_class is not None:
            expected = '<%s class="%s">SPAM and EGG</%s>' % (
                new_tag,
                new_class,
                new_tag
            )
        else:
            expected = '<%s>SPAM and EGG</%s>' % (
                new_tag,
                new_tag
            )
        self.assertEqual(expected, output)

    def test_replace_signaure_texte(self):
        self._test_replace_with_class('signature-texte', 'span', None)

    def test_recursive(self):
        xml = """<a href="www.example.tld" spam="spam" egg="egg">SPAM <spam>EGG</spam></a><inter-ligne><signature>AMIROUCHE</signature></inter-ligne>"""
        output = cleantext(xml)
        expected = """<a href="www.example.tld">SPAM EGG</a><b class="signature">AMIROUCHE</b>"""
        self.assertEqual(expected.strip(), output.strip())

    def test_strip_tag(self):
        xml = ('<p spam="spam" egg="egg">'
               'hello <foo>SPAM <b>and</b> '
               'EGG</foo></p>')
        output = cleantext(xml)
        expected = '<p>hello SPAM <b>and</b> EGG</p>'
        self.assertEqual(expected, output)

    def test_comment(self):
        xml = '<p>spam</p><!-- spam & egg --><p>egg</p>'
        output = cleantext(xml)
        expected  = '<p>spam</p><p>egg</p>'
        self.assertEqual(expected, output)
