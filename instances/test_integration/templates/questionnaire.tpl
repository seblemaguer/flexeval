{% extends 'core/base.tpl' %}

{% block content %}
<h2 class="bd-content-title"> <img src="/assets/static/img/svg_icon/chevron-right.svg" alt=">" /> Qui êtes vous ?</h2>

<form action="./{{qrname}}/send" method="post" class="form-example" enctype="multipart/form-data">

  <div class="form-group">
    <label for="q1">q1: </label>
    <input type="text" name="q1" class="form-control">
  </div>

  <div class="form-group">
    <label for="q2">q2: </label>
    <input type="text" name="q2" class="form-control">
  </div>

  <div class="form-group">
    <label for="q3">q3: </label>
    <input type="text" name="q3" class="form-control">
  </div>

  <div class="form-group">
    <label for="ez">ze: </label>
    <input type="text" name="ez" class="form-control">
  </div>

  <div class="form-group">
    <label for="ef">ef: </label>
    <input type="text" name="ef"class="form-control">
  </div>

  <div class="form-group">
    <label for="img">img: </label>
    <input type="file" name="img" class="form-control">
  </div>



  <button type="submit" class="btn btn-primary">Submit</button>

</form>
{% endblock %}
