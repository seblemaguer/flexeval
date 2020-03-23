<html>

<head>

  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="/assets/static/img/favicon.ico" />

  <title> {% block title %}PercEval{% endblock %} </title>

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
        <header>
          {% block header %}
            <h1  class="display-1"> PercEval </h1>
          {% endblock %}
        </header>


        <div class="row">
          <div class="col-1">
          </div>
          <section class="col-9">
            {% block content %}

            {% endblock %}
          </section>
        </div>
        <footer class="row">

          <div class="col-12 text-center">
            {% if userprov.connected %}
            <p class="text-muted" style="letter-spacing: 1px;">Logged in as {{ userprov.get()}} (<a href="/deco"> Log out </a>) .</p>
            {% endif %}
            <p class="text-muted" style="letter-spacing: 2px;">Powered by <a href="https://gitlab.inria.fr/dlolive/PercepEval">PercEval</a>.</p>
          </div>

          {% block footer %}

          <div class="col-12 text-center">
        				<a href="http://www.irisa.fr" target="_blank">
        					<img src="/assets/static/img/logo/irisa.png" class="img-responsive center-block" alt="IRISA lab">
        				</a>
        				<a href="http://www-expression.irisa.fr" target="_blank">
        					<img src="/assets/static/img/logo/expression.png" class="img-responsive center-block" alt="Expression team">
        				</a>
          </div>
          {% endblock %}

        </footer>
      </div>
    </div>

  </body>
</html>
