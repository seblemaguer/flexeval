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
    <img src="{{get_asset('/img/svg_icon/chevron-right.svg','flexeval')}}" alt=">" />
    {{get_variable("subtitle","Test")}} - step {{get_variable("step")}} over {{get_variable("max_steps")}}
  </h2>

  <form action="./save" method="post" enctype="multipart/form-data" class="form-example">

    <fieldset class="form-group">
      <legend class="col-form-label">
        {% block instruction %}
        <p>
          Please try to enter all of the words you hear, but <b>do not enter any comments.</b>
          If you cannot hear any sound coming out of the headphones, please make sure that your browser can handle embedded audio players (all current browsers do), and that you have not turned javascript off.
          If you can hear the audio, but you cannot understand ANY of the words, just write <b>"&lt;&gt;"</b> (without the quotes) and nothing else.
          If you can understand some, but not all of the words, just type in the ones you heard.
        </p>
        <p>
          <b>Listen to the audio file by clicking on the image below, and type what you hear into the text box.&nbsp; </b>
        </p>
        {% endblock %}
      </legend>



      {% for syssample in get_variable("syssamples") %}
        <div class="form-group" style="margin-bottom:10px;">
          {% set name_field = get_variable("field_name",name="transcription",syssamples=[syssample]) %}
          {% set content,mimetype = syssample.get(num=0)  %}

          <label for="score@{{syssample.ID}}">
            {% if mimetype == "text" %}
              {{content}}
            {% elif mimetype == "image" %}
              <img class="img-fluid" src="{{content}}" />
            {% elif mimetype == "audio" %}
              <audio id="sample" controls readall>
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

          <div class="form-group required">
            <label for="transcription@{{syssample.ID}}">Transcription:</label>
            <input type="text" id="transcription@{{syssample.ID}}" name="{{ name_field }}" class="form-control" required />
          </div>
        </div>
      {% endfor %}
    </fieldset>

    <button type="submit" id="submit" class="btn btn-primary">Submit</button>
  </form>
{% endblock %}
