{% extends get_template('base.tpl','perceval') %}

{% block content %}

  {%if get_variable("code") == 404%}
  <h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> 404 Not Found  </h2>
  <p>
     The requested resource could not be found but may be available in the future.
  </p>
  {% elif get_variable("code") == 401%}
  <h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> 401 Unauthorized  </h2>
  <p>
      Authentication is required and has failed or has not yet been provided.
  </p>
  {% elif get_variable("code") == 403%}
  <h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> 403 Forbidden  </h2>
  <p>
    You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.
  </p>

  {%elif get_variable("code") == 408%}
  <h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> 408 Request Timeout  </h2>
  <p>
        The server timed out waiting for the request.
  </p>
  {% elif get_variable("code") == 410%}
  <h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" />  410 Gone </h2>
  <p>
     The resource requested is no longer available and will not be available again.
  </p>

  {%else%}
  <h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> HTTP status code: {{get_variable("code")}}  </h2>

  <p>
    Something wrong happened ...
  </p>
  {% endif %}

  <a href="{{homepage}}"> Back </a>
{% endblock %}
