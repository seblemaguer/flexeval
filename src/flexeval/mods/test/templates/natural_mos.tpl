{% extends get_template('base.tpl') %}

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


  <h2 class="bd-content-title">
    <img src="{{get_asset('/img/svg_icon/chevron-right.svg', 'flexeval')}}" alt=">" />
    {{get_variable("subtitle","Test")}} - step {{get_variable("step")}} over {{get_variable("max_steps")}}
  </h2>

  <form action="./save" method="post" enctype="multipart/form-data" class="form-example">
    <fieldset class="form-group">
      <legend class="col-form-label">
          Listen to the example below:
      </legend>

      {% set syssample = get_variable("syssamples")[0] %}
      <div class="form-group" style="margin-bottom:10px;">
        {% set name_field = get_variable("field_name",name="MOS_score",syssamples=[syssample]) %}
        {% set content,mimetype = syssample.get('audio')  %}

        <center>
          <label for="score@{{syssample.ID}}">
            {% block player_view scoped %}
              {% include get_template('players/default/player.html') %}
            {% endblock %}
          </label>
        </center>

        <legend class="col-form-label">
          {% block instruction %}
            Now choose a score for how <b>natural</b> or <b>unnatural</b> the sentence <b><i>sounded</i></b>.
            The scale is from <b>1 [Completely Unnatural] to 5 [Completely Natural]</b>.
          {% endblock %}
        </legend>

        <select id="mos_score@{{syssample.ID}}" name="{{name_field}}" class="form-control" required>
          <option value="" selected disabled hidden>Choose here</option>
          {% block score_options %}
            <option value="1">1 : Completely Unnatural</option>
            <option value="2">2 : Mostly Unnatural</option>
            <option value="3">3 : Equally Natural and Unnatural</option>
            <option value="4">4 : Mostly Natural</option>
            <option value="5">5 : Completely Natural</option>
          {% endblock %}
        </select>
      </div>
    </fieldset>

    <button type="submit" id="submit" class="btn btn-primary">Submit</button>
  </form>

  <script>
    {% block player_controls scoped %}
      {% include get_template('players/default/controls.js') %}
    {% endblock %}
  </script>
{% endblock %}
