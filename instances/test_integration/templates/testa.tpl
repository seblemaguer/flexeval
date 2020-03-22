{% extends 'base.tpl' %}

{% block content %}

<h2 class="bd-content-title"> <img src="/assets/static/img/svg_icon/chevron-right.svg" alt=">" /> Test {{ name }} - step {{step}} over {{nb_step}}</h2>

<form action="./{{name}}/send" method="post" class="form-example" enctype="multipart/form-data">


  {% for system in systems() %}
  <div class="form-group">
    {% set name = save_field('score',system) %}
    <label for="{{ name }}"> Blabla: {{system.data["sentence"]}} </label>
    <img src="{{ obfuscate_assets(system.data['image']) }}" />
    <select name="{{ name }}" class="form-control">
     <option value="1">Médiocre</option>
     <option value="2">Moyen</option>
     <option value="3">Correct</option>
     <option value="4"> Bon </option>
    </select>

  </div>

  <div class="form-group">
    {% set name = save_field('image',system) %}
    <label for="{{ name }}"> Bidule </label>
    <input name="{{ name }}" type="file"  class="form-control">

  </div>

  {% endfor %}

  <button type="submit" class="btn btn-primary">Submit</button>

</form>

{% endblock %}
