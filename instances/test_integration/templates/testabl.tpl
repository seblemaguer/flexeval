{% extends 'base.tpl' %}

{% block content %}
<h2 class="bd-content-title"> <img src="/assets/static/img/svg_icon/chevron-right.svg" alt=">" /> Test {{ name }} - step {{step}} over {{nb_step}}</h2>

<form action="./{{name}}/send" method="post" class="form-example" enctype="multipart/form-data">


  {% for system in systems("tB","tC") %}
  <div class="form-example">

    <p> Blabla: {{system.data[system.get_column_name(0)]}},{{system.data["sentence2"]}} </p>
    <select name="{{ save_field('score',system) }}">
     <option value="1">Médiocre</option>
     <option value="2">Moyen</option>
     <option value="3">Correct</option>
     <option value="4"> Bon </option>
    </select>

    <input name="{{ save_field('image',system) }}" type="file">

  </div>
  {% endfor %}


  {% for system in systems("tB","tC") %}
  <div class="form-example">
    <input type="radio" name="{{ save_field('choose_one_system',systems()) }}" value=" {{ system.name() }}">
  </div>
  {% endfor %}

  <button  class="btn btn-outline-primary">Send</button>

</form>

{% endblock %}
