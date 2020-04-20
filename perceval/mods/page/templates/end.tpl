{% extends get_template('base.tpl','perceval') %}

{% block content %}

<h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" />Test completed!</h2>

<p>
  You have completed the test !
  Thank you for your time.
  You can close the page.
</p>

{% endblock %}
