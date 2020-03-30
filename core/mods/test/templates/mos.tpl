{% extends 'base.tpl' %}

{% set subtitle = variables("subtitle",default_value="Test " + stage_name) %}
{% set media = variables("media",default_value="text") %}

{% block content %}
{% if intro %}

<div class="alert alert-warning" role="alert">
  <h4 class="alert-heading">This is the <strong>introduction</strong></h4>
  <p>Your answers will <strong>not</strong> be recorded for now.</p>
</div>

{% endif %}

{% if firstStepAfterIntro %}
  <div class="alert alert-danger alert-dismissible fade show" role="alert">
    <h4 class="alert-heading">This is now the <strong>real</strong> test, not an introduction step.</h4>
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
{% endif %}

<h2 class="bd-content-title"> <img src="{{make_url('/assets/static/img/svg_icon/chevron-right.svg')}}" alt=">" /> {{ subtitle }} - step {{step}} over {{nb_step}}</h2>

<form action="./{{stage_name}}/send" method="post" class="form-example" enctype="multipart/form-data">

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
