{% extends 'base.tpl' %}


{% set subtitle = variables("subtitle",default_value="Test " + stage_name) %}
{% set media = variables("media",default_value="text") %}

{% set sysref = systems()[0] %}
{% if "sysref" in variables %}
  {% for system in systems() %}
    {% if system.name_system == variables["sysref"] %}
        {% set sysref = system %}
    {% endif %}
  {% endfor %}
{% endif %}

{% block head %}
<script>
$(document).ready(function(){


    $("input[type=range]").map(function() {
      var poper = $(this).popover();

      // Read value on change
      $(this).change(function(){
        $(this).popover('dispose');
        mushra_score = $(this).val()
        if(mushra_score > 80)
        {
          label = "Excellent"
        }else if(mushra_score > 60)
        {
          label = "Good"
        }
        else if(mushra_score > 40)
        {
          label = "Fair"
        }
        else if(mushra_score > 20)
        {
          label = "Poor"
        }
        else {
          label = "Bad"
        }

        $(this).attr("data-content",label+" ("+mushra_score+")");
        $(this).popover('update');
        $(this).popover('toggle');

      });

      }).get()
    .join();

});


</script>
{% endblock %}


{% block content %}

<h2 class="bd-content-title"> <img src="/assets/static/img/svg_icon/chevron-right.svg" alt=">" /> {{ subtitle }} - step {{step}} over {{nb_step}}</h2>

<form action="./{{stage_name}}/send" method="post" class="form-example" enctype="multipart/form-data">

  <legend class="col-form-label"><strong>Question:</strong> How do you judge the <strong>quality</strong> of the following candidates against the reference?</legend>

  <fieldset class="form-group">
    <legend class="col-form-label"><strong>Reference:</strong></legend>

    {% if media == "text" %}
      {{sysref.data[sysref.get_column_name(0)]}}
    {% elif media == "image" %}
      <img class="img-fluid" src="{{ obfuscate_assets("/assets/"+sysref.data[sysref.get_column_name(0)]) }}" />
    {% elif media == "audio" %}
      <audio controls readall>
        <source src="{{ obfuscate_assets("/assets/"+sysref.data[sysref.get_column_name(0)]) }}">
        Your browser does not support the <code>audio</code> element.
      </audio>
    {% elif media == "video" %}
      <video controls readall>
        <source src="{{ obfuscate_assets("/assets/"+sysref.data[sysref.get_column_name(0)]) }}">
          Your browser does not support the <code>video</code> element.
      </video>
    {% else %}
        {{sysref.data[sysref.get_column_name(0)]}}
    {% endif %}

  </fieldset>

  <fieldset class="form-group">
    <legend class="col-form-label"><strong>Candidates:</strong></legend>
    {% for system in systems() %}
      {% if not(system.name_system == sysref.name_system) %}

        <div class="form-group">
          {% set name_field = save_field('score',system) %}
          <label for="score@{{ system.name() }}">

            {% if media == "text" %}
              {{system.data[system.get_column_name(0)]}}
            {% elif media == "image" %}
              <img class="img-fluid" src="{{ obfuscate_assets("/assets/"+system.data[system.get_column_name(0)]) }}" />
            {% elif media == "audio" %}
              <audio controls readall>
                <source src="{{ obfuscate_assets("/assets/"+system.data[system.get_column_name(0)]) }}">
                Your browser does not support the <code>audio</code> element.
              </audio>
            {% elif media == "video" %}
              <video controls readall>
                <source src="{{ obfuscate_assets("/assets/"+system.data[system.get_column_name(0)]) }}">
                  Your browser does not support the <code>video</code> element.
              </video>
            {% else %}
                {{system.data[system.get_column_name(0)]}}
            {% endif %}

          </label>

            <input name="{{ name_field }}" class="form-control-range" data-trigger="hover" data-toggle="popover" data-content="Fair (50)" data-placement="right" id="score@{{ system.name() }}" type="range" data-slider-min="0" data-slider-max="100" data-slider-step="1" data-slider-value="50"/>

        </div>

      {% endif %}
    {% endfor %}


  </fieldset>

  <button type="submit" class="btn btn-primary">Submit</button>

</form>
{% endblock %}
