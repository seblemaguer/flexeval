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

  <div class="container">
    <div class="row">
      <div class="col">
      </div>
      <div class="col-10">
        <header class="row">
          {% block header %}
            <h1  class="display-1">  {{ get_variable("title",default_value="FlexEval")}} </h1>
            <div class="col-12 text-left">
              {% if get_variable("description") is not none %}
              <span>{{get_variable("description")}}</span>
              {% endif %}
              <span></span>
            </div>
          {% endblock %}

          <div class="col-12 text-right">
              <p class="text-muted" style="letter-spacing: 1px;"> &nbsp; {%block userintel%} {% if auth.validates_connection("connected")[0] %} Logged in as {{ auth.user.pseudo}} (<a href="{{ auth.url_deco  }} "> Log out </a>) . {% endif %}{%endblock%}</p>
          </div>

        </header>


        <div class="row">
          <div class="container">
            <div class="row">
              <div class="col-1"></div>
              <section class="col-9">
                <div class="container">
                  {% block content %}

                  {% endblock %}
                </div>
              </section>
              <div class="col-2"></div>
            </div>
          </div>
        </div>

        <footer class="row" style="margin-top:20px;">
          <div class="col-12 text-center">
            {% block footer %}
        				<a href="http://www.irisa.fr" target="_blank">
        					<img src="{{get_asset('/img/logo/irisa.png','flexeval')}}" class="img-responsive center-block" alt="IRISA lab">
        				</a>
        				<a href="http://www-expression.irisa.fr" target="_blank">
        					<img src="{{get_asset('/img/logo/expression.png','flexeval')}}" class="img-responsive center-block" alt="Expression team">
        				</a>
            {% endblock %}

          </div>

          <div class="col-12 text-center">
            <p class="text-muted" style="letter-spacing: 2px;">
              {% if get_variable("authors") is not none %}
                Made by {{get_variable("authors")}}.
              {% endif %}
              </p>

            <p class="text-muted" style="letter-spacing: 2px;">
Powered by <a href="https://gitlab.inria.fr/expression/tools/FlexEval">FlexEval</a>.
            </p>
              {%block bottomlink%}
                <p class="text-muted" style="letter-spacing: 2px;">
                  {% if module_class == "AdminModule" %}
                     <a href="{{make_url('/')}}"> Leave Admin panel.</a>
                  {% else %}
                    <a href="{{make_url('/admin')}}"> Access Admin  panel.</a>
                  {% endif %}
                </p>
              {%endblock%}
          </div>
        </footer>
      </div>
    </div>
  </body>
</html>
