{% extends get_template('base.tpl','perceval') %}

{% block content %}
  <h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> Login</h2>
  <p>
    This website is only available by invitation, if you have been invited, you have received one by email.
    You will find a link in this email, please click on it.
  </p>
{% endblock %}
