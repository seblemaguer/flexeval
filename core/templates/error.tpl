{% extends 'base.tpl' %}


{% block content %}

  {%if code == 404%}
  <h2 class="bd-content-title"> <img src="{{make_url('/assets/static/img/svg_icon/chevron-right.svg')}}" alt=">" /> 404 Not Found  </h2>
  <p>
     The requested resource could not be found but may be available in the future.
  </p>
  {% elif code == 401%}
  <h2 class="bd-content-title"> <img src="{{make_url('/assets/static/img/svg_icon/chevron-right.svg')}}" alt=">" /> 401 Unauthorized  </h2>
  <p>
      Authentication is required and has failed or has not yet been provided.
  </p>
  {% elif code == 403%}
  <h2 class="bd-content-title"> <img src="{{make_url('/assets/static/img/svg_icon/chevron-right.svg')}}" alt=">" /> 403 Forbidden  </h2>
  <p>
    You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.
  </p>

  {%elif code == 408%}
  <h2 class="bd-content-title"> <img src="{{make_url('/assets/static/img/svg_icon/chevron-right.svg')}}" alt=">" /> 408 Request Timeout  </h2>
  <p>
        The server timed out waiting for the request.
  </p>
  {% elif code == 410%}
  <h2 class="bd-content-title"> <img src="{{make_url('/assets/static/img/svg_icon/chevron-right.svg')}}" alt=">" />  410 Gone </h2>
  <p>
     The resource requested is no longer available and will not be available again.
  </p>

  {%else%}
  <h2 class="bd-content-title"> <img src="{{make_url('/assets/static/img/svg_icon/chevron-right.svg')}}" alt=">" /> HTTP status code: {{code}}  </h2>

  <p>
    Something wrong happened ...
  </p>
  {% endif %}

  <a href="{{entrypoint}}"> Back </a>
{% endblock %}
