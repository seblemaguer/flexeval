{% extends get_template('base.tpl','perceval') %}

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


<h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" />{{get_variable("subtitle","Test")}} - step {{get_variable("step")}} over {{get_variable("max_steps")}}</h2>

<form action="./save" method="post" enctype="multipart/form-data" class="form-example">

  <fieldset class="form-group">
    <legend class="col-form-label"><strong>Question:</strong> How do you judge the <strong>quality</strong> of the following sample?</legend>



    {% for syssample in get_variable("syssamples") %}
    <div class="form-group" style="margin-bottom:10px;">
      {% set name_field = get_variable("field_name",name="MOS_score",syssamples=[syssample]) %}
      {% set content,mimetype = syssample.get(num=0)  %}

      <label for="score@{{syssample.ID}}">

        {% if mimetype == "text" %}
          {{content}}
        {% elif mimetype == "image" %}
          <img class="img-fluid" src="{{content}}" />
        {% elif media == "audio" %}
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
      <select id="score@{{syssample.ID}}" name="{{ name_field }}" class="form-control" required>
      <option value="" selected disabled hidden>Choose here</option>
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
