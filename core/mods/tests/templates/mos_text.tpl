{% extends 'base.tpl' %}

{% block content %}

<h2 class="bd-content-title"> <img src="/assets/static/img/svg_icon/chevron-right.svg" alt=">" /> Test {{ name }} - step {{step}} over {{nb_step}}</h2>

<form action="./{{name}}/send" method="post" class="form-example" enctype="multipart/form-data">

  <fieldset class="form-group">
    <legend class="col-form-label"><strong>Question:</strong> Between 1 and 5, how do you judge the <strong>quality</strong> of the following sample?</legend>


    {% for system in systems() %}
    <div class="form-group">
      {% set name = save_field('score',system) %}
      <label for="{{ name }}"> {{system.data[system.get_column_name(0)]}}</label>
      <select name="{{ name }}" class="form-control">
       <option value="5">Excellent</option>
       <option value="4">Good</option>
       <option value="3">Fair</option>
       <option value="2"> Poor </option>
       <option value="1"> Bad </option>
      </select>

    </div>
    {% endfor %}

  </fieldset>

  <button type="submit" class="btn btn-primary">Submit</button>

</form>
{% endblock %}
