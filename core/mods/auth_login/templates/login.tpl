{% extends 'core/base.tpl' %}

{% block title %}Login{% endblock %}

{% block content %}
  <h2 class="bd-content-title"> <img src="/assets/static/img/svg_icon/chevron-right.svg" alt=">" /> Login</h2>

  <form action="./{{ name }}/log-register" method="post" class="form-example">
    <div class="form-example">
      <label for="email">Enter your email: </label>
      <input type="email" name="email" id="email" required>
    </div>
    <div class="form-example">
      <input type="submit" value="Subscribe">
    </div>
  </form>
{% endblock %}

{% block footer %}
{% endblock %}
