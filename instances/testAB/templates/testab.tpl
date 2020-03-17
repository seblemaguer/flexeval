{% extends 'base.tpl' %}

{% block title %}Test MOS{% endblock %}

{% block content %}

<form action="./{{name}}/send" method="post" class="form-example" enctype="multipart/form-data">


  {% for system in systems() %}
  <div class="form-example">

    <p> Blabla: {{system.data[system.get_column_name(0)]}},{{system.data["sentence2"]}} </p>
    <select name="{{ system.save_field('score') }}">
     <option value="1">Médiocre</option>
     <option value="2">Moyen</option>
     <option value="3">Correct</option>
     <option value="4"> Bon </option>
    </select>

    <input name="{{ system.save_field('image') }}" type="file">
  
  </div>
  {% endfor %}


  <button>Send</button>

</form>

{% endblock %}

{% block footer %}
{% endblock %}
