{% extends get_template('base.tpl','perceval') %}

{% block content %}

<h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> Alternated tests.</h2>

<p>
  You are at the <strong>{{get_variable("alternate_step")}}-nth iteration</strong>.
</p>
<p>
  To complete this alternated tests, you need to complete in total: {{get_variable("alternate_max_step")}} iterations.
</p>
<p>
  Each iteration is composed of at most of {{get_variable("alternate_nb_steps_per_iteration")}} question(s) for each test.

</p>

<a class="btn btn-primary" href="{{url_next}}"> Complete an iteration for the test: {{get_variable("alternate_next_test")}} </a>
{% endblock %}
