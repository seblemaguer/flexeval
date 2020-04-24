{% extends get_template('base.tpl','flexeval') %}

{% block content %}

<h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','flexeval')}}" alt=">" /> Test</h2>

<p>
  Bonjour :)
</p>

<a href="{{url_next}}"> Commencer le test </a>
{% endblock %}
