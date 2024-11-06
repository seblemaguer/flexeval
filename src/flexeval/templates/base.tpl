<!doctype html>
<html>

  <head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="{{get_asset('/img/favicon.ico','flexeval')}}" />

    <title> {{ get_variable("title",default_value="flexeval")}} </title>

    <!-- JQuery -->
    <script src="{{get_asset('/js/jquery-3.4.1.min.js','flexeval')}}"></script>
    <script src="{{get_asset('/js/jquery-ui.min.js','flexeval')}}"></script>
    <link href="{{get_asset('/css/jquery-ui.min.css','flexeval') }}" rel="stylesheet">

    <!-- Bootstrap Core CSS -->
    <script src="{{get_asset('/js/popper.min.js','flexeval')}}"></script>
    <link href="{{get_asset('/css/bootstrap-4.4.1/bootstrap.min.css','flexeval') }}" rel="stylesheet">
    <script src="{{get_asset('/js/bootstrap-4.4.1/bootstrap.min.js','flexeval') }}"></script>

    <!-- Additional libraries -->
    <script src="{{get_asset('/js/flexeval.js','flexeval')}}"></script>
    <link href="{{get_asset('/css/flexeval.css','flexeval')}}" rel="stylesheet">

    {% block head %}
    {% endblock %}
  </head>

  <body>
    <header class="row" style="margin-bottom: 30px;">
      {% block header %}
        <h1 class="display-1">{{get_variable("title", default_value="FlexEval")}}</h1>
      {% endblock %}

            {# <div class="col-12 text-right"> #}
      {#   <p class="text-muted" style="letter-spacing: 1px;"> &nbsp; {%block userintel%} {% if auth.validates_connection("connected")[0] %} Logged in as {{ auth.user.id}} (<a href="{{ auth.url_deco  }} "> Log out </a>) . {% endif %}{%endblock%}</p> #}
      {# </div> #}
    </header>


    <div class="container">
      <div class="container">
        {% block content %}

        {% endblock %}
      </div>
    </div>

    <footer class="row" style="margin-top:20px;">
      <div class="col-12 text-center">
        {% block footer %}

        {% endblock %}
      </div>
    </footer>
  </body>
</html>
