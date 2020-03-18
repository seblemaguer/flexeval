{% extends 'base.tpl' %}

{% block title %}Login{% endblock %}

{% block content %}
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
