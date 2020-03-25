{% extends 'base.tpl' %}


{% block content %}
  <h2 class="bd-content-title"> <img src="/assets/static/img/svg_icon/chevron-right.svg" alt=">" /> {{code}} Error </h2>

  <p>
    Something wrong happened ...
  </p>


  <a href="{{entrypoint}}"> Back </a>
{% endblock %}
