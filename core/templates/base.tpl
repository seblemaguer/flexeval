<html>

  <head>

      <meta charset="utf-8">

      <title> {% block title %}PercEval{% endblock %} </title>

      <!-- JQuery -->
      <script src="/assets/static/js/jquery-3.4.1.min.js"></script>

      <!-- Bootstrap Core CSS -->
    	<link href="/assets/static/css/bootstrap-4.4.1/bootstrap.min.css" rel="stylesheet">
    	<script src="/assets/static/js/bootstrap-4.4.1/bootstrap.min.js"></script>

  </head>

  <body>

    <header>
      {% block header %}

      {% endblock %}
    </header>

    <section class="content">
      {% block content %}

      {% endblock %}
    </section>

    <footer>
      {% block footer %}

      {% endblock %}
    </footer>

  </body>

</html>
