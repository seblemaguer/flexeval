{% extends 'base.tpl' %}

{% block title %} Export {% endblock %}


{% block content %}
  <h2 class="bd-content-title"> <img src="/assets/static/img/svg_icon/chevron-right.svg" alt=">" /> Admin Panel</h2>
  <form action="./panel" method="get" class="form-example">
    <div class="form-group">
      <label for="password">Enter password: </label>
      <input type="password" name="password" id="password" class="form-control" required>
    </div>

    <button type="submit" class="btn btn-primary">Submit</button>

  </form>

{% endblock %}
