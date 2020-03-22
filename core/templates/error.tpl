{% extends 'base.tpl' %}

{% block title %}{{code}} Error{% endblock %}


{% block content %}
  <h2 class="bd-content-title"> <img src="/assets/static/img/svg_icon/chevron-right.svg" alt=">" /> Something wrong happened ...</h2>

  <a href="{{entrypoint}}"> Back </a>
{% endblock %}
