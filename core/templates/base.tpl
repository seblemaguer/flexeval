<html>

<head>

  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title> {% block title %}PercEval{% endblock %} </title>

  <!-- JQuery -->
  <script src="/assets/static/js/jquery-3.4.1.min.js"></script>

  <!-- Bootstrap Core CSS -->
  <link href="/assets/static/css/bootstrap-4.4.1/bootstrap.min.css" rel="stylesheet">
  <script src="/assets/static/js/bootstrap-4.4.1/bootstrap.min.js"></script>

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
        <footer class="rox">

          {% block footer %}

          {% endblock %}

          {% if userprov.connected %}
            <p style="text-align:center; color:gray">Logged in as {{ userprov.get()}} (<a href="/deco"> Log out </a>) .</p>
          {% endif %}

        </footer>
      </div>
    </div>

  </body>
</html>
