{% extends get_template('base.tpl','perceval') %}

{% block head %}
<script>
$(document).ready(function(){


    $("input[type=range]").map(function() {
      var poper = $(this).popover();

      // Read value on change
      $(this).on("mouseleave change click",function(){
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

{% if get_variable("intro_step",False) %}
<div class="alert alert-warning alert-dismissible fade show" role="alert">
  <h4 class="alert-heading">This is the <strong>introduction</strong>.</h4>
  <p>Your answers will <strong>not</strong> be recorded as correct answer.</p>

  <button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>
</div>
{% endif %}

{% if not(get_variable("intro_step",False)) and (get_variable("step") == 1) %}
  <div class="alert alert-danger alert-dismissible fade show" role="alert">
    <h4 class="alert-heading">This is now the <strong>real</strong> test, not an introduction step.</h4>

    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
{% endif %}


<h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> {{get_variable("subtitle","Test")}} - step {{get_variable("step")}} over {{get_variable("max_steps")}}</h2>

<form action="./save" method="post" enctype="multipart/form-data" class="form-example">

  <fieldset class="form-group">
    <legend class="col-form-label"><strong>Question:</strong> How do you judge the <strong>quality</strong> of the following candidates against the reference?</legend>


    <fieldset class="form-group">
      <legend class="col-form-label"><strong>Reference:</strong></legend>
      {% set _sysref = get_variable("syssamples",get_variable("sysref"))[0] %}
      {% set content,mimetype = _sysref.get(num=0)  %}

      {% if mimetype == "text" %}
        {{content}}
      {% elif mimetype == "image" %}
        <img class="img-fluid" src="{{content}}" />
      {% elif mimetype == "audio" %}
        <audio controls readall>
          <source src="{{content}}">
          Your browser does not support the <code>audio</code> element.
        </audio>
      {% elif mimetype == "video" %}
        <video controls readall>
          <source src="{{content}}">
            Your browser does not support the <code>video</code> element.
        </video>
      {% else %}
          {{content}}
      {% endif %}

    </fieldset>


    <fieldset class="form-group">
      <legend class="col-form-label"><strong>Candidates:</strong></legend>
      {% for syssample in get_variable("syssamples") %}

        {% if not(syssample.system_name == get_variable("sysref")) %}

          {% set name_field = get_variable("field_name",name="MUSHRA_score",syssamples=[syssample]) %}
          {% set content,mimetype = syssample.get(num=0)  %}

          <div class="form-group" style="margin-bottom:10px;">
            <label for="score@{{syssample.ID}}">

              {% if mimetype == "text" %}
                {{content}}
              {% elif mimetype == "image" %}
                <img class="img-fluid" src="{{content}}" />
              {% elif mimetype == "audio" %}
                <audio controls readall>
                  <source src="{{content}}">
                  Your browser does not support the <code>audio</code> element.
                </audio>
              {% elif mimetype == "video" %}
                <video controls readall>
                  <source src="{{content}}">
                    Your browser does not support the <code>video</code> element.
                </video>
              {% else %}
                  {{content}}
              {% endif %}

            </label>

            <input name="{{ name_field }}" class="form-control-range" data-trigger="hover" data-toggle="popover" data-content="Fair (50)" data-placement="right" id="score@{{syssample.ID}}" type="range" data-slider-min="0" data-slider-max="100" data-slider-step="1" data-slider-value="50" required />

          </div>

        {% endif %}
      {% endfor %}
    </fieldset>

  </fieldset>

  <button type="submit" class="btn btn-primary">Submit</button>

</form>
{% endblock %}
