{% extends get_template('base.tpl') %}

{% block content %}
  <form action="./register" method="post" class="form-example">
    {% block instructions %}
      <h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','flexeval')}}" alt=">" /> Login</h2>
    <p>
      Welcome to the platform.
      Please authenticate using your email.
    </p>
  {% endblock %}

  <div class="mb-3">
    <label for="email">Enter your email: </label>
    <input type="email" name="email" id="email" class="form-control" required>
  </div>

  <button type="submit" class="btn btn-primary">Submit</button>
  </form>
{% endblock %}
