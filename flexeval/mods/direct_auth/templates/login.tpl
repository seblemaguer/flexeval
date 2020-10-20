{% extends get_template('base.tpl') %}

{% block content %}
  <h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','flexeval')}}" alt=">" /> Login</h2>
  <form action="./register" method="post" class="form-example">
    <div class="form-group">
      <label for="email">Enter your email: </label>
      <input type="email" name="email" id="email" class="form-control" required>
    </div>


    <div class="form-check">
      <input type="checkbox" class="form-check-input" id="legalterms" required>
      <label class="form-check-label" for="legalterms">I acknowledge having read and accept <a href="{{make_url('/legal_terms')}}">the GCUs and the privacy policy</a>.</label>
    </div>

    <button type="submit" class="btn btn-primary">Submit</button>

  </form>
{% endblock %}
