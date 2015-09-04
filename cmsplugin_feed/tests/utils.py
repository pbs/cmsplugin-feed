from django.template.loaders.base import Loader as BaseLoader


class MockLoader(BaseLoader):

    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        html = """
{% load cms_tags sekizai_tags %}
<html>
  <head>{% render_block "css" %}</head>
  <body>
      {% placeholder base_content %}
      {% block base_content%}{% endblock %}
      {% render_block "js" %}
  </body>
</html>"""

        return html, 'template.html'
