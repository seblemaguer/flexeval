{% extends 'base.tpl' %}

{% block title %}Qui êtes vous ?{% endblock %}

{% block content %}
<form action="./{{qrname}}/send" method="post" class="form-example" enctype="multipart/form-data">

  <div class="form-example">
    <label for="q1">q1: </label>
    <input type="text" name="q1" id="q1">
  </div>

  <div class="form-example">
    <label for="q2">q2: </label>
    <input type="text" name="q2" id="q2">
  </div>

  <div class="form-example">
    <label for="q3">q3: </label>
    <input type="text" name="q3" id="q3">
  </div>

  <div class="form-example">
    <label for="ez">ze: </label>
    <input type="text" name="ez" id="ez">
  </div>

  <div class="form-example">
    <label for="ef">ef: </label>
    <input type="text" name="ef" id="ef">
  </div>

  <div class="form-example">
    <label for="img">img: </label>
    <input type="file" name="img" id="img">
  </div>



  <div class="form-example">
    <input type="submit" value="Send">
  </div>
</form>
{% endblock %}

{% block footer %}
{% endblock %}
