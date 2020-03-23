{% extends 'base.tpl' %}

{% set title = "Test" + name %}
{% set media = "text" %}
{% if "name" in parameters %}   {% set title = parameters["name"] %}{% endif %}
{% if "media" in parameters %}   {% set media = parameters["media"] %} {% endif %}

{% block content %}

<h2 class="bd-content-title"> <img src="/assets/static/img/svg_icon/chevron-right.svg" alt=">" /> {{ title }} - step {{step}} over {{nb_step}}</h2>

<form action="./{{name}}/send" method="post" class="form-example" enctype="multipart/form-data">

  <fieldset class="form-group">
    <legend class="col-form-label"><strong>Question:</strong> How do you judge the <strong>quality</strong> of the following sample?</legend>


    {% for system in systems() %}
    <div class="form-group">
      {% set name_field = save_field('score',system) %}
      <label for="score@{{ system.name() }}">

        {% if media == "text" %}
          {{system.data[system.get_column_name(0)]}}
        {% elif media == "image" %}
          <img class="img-fluid" src="{{ obfuscate_assets(system.data[system.get_column_name(0)]) }}" />
        {% elif media == "audio" %}
          <audio controls readall>
            <source src="{{ obfuscate_assets(system.data[system.get_column_name(0)]) }}">
            Your browser does not support the <code>audio</code> element.
          </audio>
        {% elif media == "video" %}
          <video controls readall>
            <source src="{{ obfuscate_assets(system.data[system.get_column_name(0)]) }}">
              Your browser does not support the <code>video</code> element.
          </video>
        {% else %}
            {{system.data[system.get_column_name(0)]}}
        {% endif %}

      </label>
      <select id="score@{{ system.name() }}" name="{{ name_field }}" class="form-control">
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
