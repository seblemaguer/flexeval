{% extends get_template('base.tpl','perceval') %}

{% block content %}

<h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> Choose our next step.</h2>

<a class="btn btn-primary" href="{{url_next['testAB']}}"> Test AB </a>
<a class="btn btn-primary" href="{{url_next['testMOS']}}"> Test MOS </a>


{% endblock %}
