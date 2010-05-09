#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import \
     Comment, Literal, Operator, Keyword, Name, String

class GherkinLexer(RegexLexer):
    """
    For `Gherkin <http://cukes.info/>` syntax.
    """
    name = 'Gherkin'
    aliases = ['Cucumber', 'cucumber', 'Gherkin', 'gherkin']
    filenames = ['*.feature']
    mimetypes = ['text/x-gherkin']

    feature_keywords         = ur'^(<%= gherkin_keywords(:feature) %>)(:)(.*)$'
    feature_element_keywords = ur'^(\s*)(<%= gherkin_keywords(:background, :scenario, :scenario_outline) %>)(:)(.*)$'
    examples_keywords        = ur'^(\s*)(<%= gherkin_keywords(:examples) %>)(:)(.*)$'
    step_keywords            = ur'^(\s*)(<%= gherkin_keywords(:step) %>)'

    tokens = {
        'comments': [
            (r'#.*$', Comment),
          ],
        'multiline_descriptions' : [
            (step_keywords, Keyword, "step_content_stack"), # There must be a better way of doing this...
            include('comments'),
            (r"(\s|.)", Name.Function),
          ],
        'multiline_descriptions_on_stack' : [
            (step_keywords, Keyword, "#pop:2"),
            include('comments'),
            (r"(\s|.)", Name.Function),
          ],
        'examples_table': [
            (r"\s+\|", Keyword, 'examples_table_header'),
            include('comments'),
            (r"(\s|.)", Name.Function),
          ],
        'examples_table_header': [
            (r"\s+\|\s*$", Keyword, "#pop:2"),
            include('comments'),
            (r"\s*\|", Keyword),
            (r"[^\|]", Name.Variable),
          ],
        'scenario_sections_on_stack': [
            (feature_element_keywords, bygroups(Name.Function, Keyword, Keyword, Name.Function), "multiline_descriptions_on_stack"),
          ],
        'narrative': [
            include('scenario_sections_on_stack'),
            (r"(\s|.)", Name.Function),
          ],
        'table_vars': [
            (r'(<[^>]*>)', bygroups(Name.Variable)),
          ],
        'string': [
            include('table_vars'),
            (r'(\s|.)', String),
          ],
        'py_string': [
            (r'"""', Keyword, "#pop"),
            include('string'),
          ],
          'step_content_root':[
            (r"$", Keyword, "#pop"),
            include('step_content'),
          ],
          'step_content_stack':[
            (r"$", Keyword, "#pop:2"),
            include('step_content'),
          ],
          'step_content':[
            (r'"', Name.Function, "double_string"),
            include('table_vars'),
            include('comments'),
            (r'(\s|.)', Name.Function),
          ],
          'table_content': [
            (r"\s+\|\s*$", Keyword, "#pop"),
            include('comments'),
            (r"\s*\|", Keyword),
            include('string'),
          ],
        'double_string': [
            (r'"', Name.Function, "#pop"),
            include('string'),
          ],
        'root': [
            (r'\n', Name.Function),
            include('comments'),
            (r'"""', Keyword, "py_string"),
            (r'\s+\|', Keyword, 'table_content'),
            (r'"', Name.Function, "double_string"),
            include('table_vars'),
            (r'(\s*)(@[^@\r\n\t ]+)', bygroups(Name.Function, Name.Tag)),
            (step_keywords, bygroups(Name.Function, Keyword), "step_content_root"),
            (feature_keywords, bygroups(Keyword, Keyword, Name.Function), 'narrative'),
            (feature_element_keywords, bygroups(Name.Function, Keyword, Keyword, Name.Function), "multiline_descriptions"),
            (examples_keywords, bygroups(Name.Function, Keyword, Keyword, Name.Function), "examples_table"),
            (r'(\s|.)', Name.Function),
        ]
    }
