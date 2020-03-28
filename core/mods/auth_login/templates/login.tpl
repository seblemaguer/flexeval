{% extends 'base.tpl' %}

{% block content %}
  <h2 class="bd-content-title"> <img src="/assets/static/img/svg_icon/chevron-right.svg" alt=">" /> Login</h2>
  <form action="./{{ stage_name }}/log-register" method="post" class="form-example">
    <div class="form-group">
      <label for="email">Enter your email: </label>
      <input type="email" name="email" id="email" class="form-control" required>
    </div>

    <button type="submit" class="btn btn-primary">Submit</button>

  </form>
{% endblock %}
