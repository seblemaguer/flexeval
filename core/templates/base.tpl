<html>

<head>

  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="/assets/static/img/favicon.ico" />

  <title> {{ variables("title",default_value="PercEval")}} </title>

  <!-- JQuery -->
  <script src="/assets/static/js/jquery-3.4.1.min.js"></script>

  <!-- Bootstrap Core CSS -->
  <script src="/assets/static/js/popper.min.js"></script>
  <link href="/assets/static/css/bootstrap-4.4.1/bootstrap.min.css" rel="stylesheet">
  <script src="/assets/static/js/bootstrap-4.4.1/bootstrap.min.js"></script>

  <!-- Additional libraries -->
  <script src="/assets/static/js/perceval.js"></script>
  <link href="/assets/static/css/perceval.css" rel="stylesheet">

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
            <h1  class="display-1">  {{ variables("title",default_value="PercEval")}} </h1>
            {% if variables("description") is not none %}
            <span>{{variables("description")}}</span>
            {% endif %}
            <span></span>
          {% endblock %}

          <div class="col-12 text-right">
            <p class="text-muted" style="letter-spacing: 1px;"> &nbsp; {%block userintel%} {% if userprov.connected %} Logged in as {{ userprov.get()}} (<a href="/deco"> Log out </a>) . {% endif %}{%endblock%}</p>
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
        					<img src="/assets/static/img/logo/irisa.png" class="img-responsive center-block" alt="IRISA lab">
        				</a>
        				<a href="http://www-expression.irisa.fr" target="_blank">
        					<img src="/assets/static/img/logo/expression.png" class="img-responsive center-block" alt="Expression team">
        				</a>
            {% endblock %}

          </div>

          <div class="col-12 text-center">
            <p class="text-muted" style="letter-spacing: 2px;">
              {% if variables("authors") is not none %}
                Made by {{variables("authors")}}.
              {% endif %}
              Powered by <a href="https://gitlab.inria.fr/dlolive/PercepEval">PercEval</a>.
              </p>
              {%block bottomlink%}
                <p class="text-muted" style="letter-spacing: 2px;">
                  Access <a href="/admin"> Admin panel </a>.
                </p>
              {%endblock%}
          </div>
        </footer>
      </div>
    </div>

  </body>
</html>
