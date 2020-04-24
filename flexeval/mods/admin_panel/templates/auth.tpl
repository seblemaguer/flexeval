{% extends get_template('base.tpl','flexeval') %}

{% block content %}

  <h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','flexeval')}}" alt=">" /> Admin Panel</h2>

  <form action="./login" method="post" class="form-example">
    <div class="form-group">
      <label for="admin_password">Enter password: </label>
      <input type="password" name="admin_password" id="admin_password" class="form-control" required>
    </div>

    <button type="submit" class="btn btn-primary">Submit</button>

  </form>



{% endblock %}
