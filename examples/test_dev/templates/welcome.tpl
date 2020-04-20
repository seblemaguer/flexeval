{% extends get_template('base.tpl','perceval') %}

{% block content %}

<h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" />Test</h2>

<p>
  Bonjour :)
</p>

<a href="{{url_next}}"> Commencer le test </a>
{% endblock %}
