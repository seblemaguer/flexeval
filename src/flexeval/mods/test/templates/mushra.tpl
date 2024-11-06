{% extends get_template('base.tpl') %}

{% block head %}
  <style>

      input[type="range"] {
    writing-mode: vertical-lr;
    direction: rtl;
          height: 200px;
      }

    input[type="range"]:hover {
      background: #4CAF50;
    }
    .slider-container {
    height:200px;
    }

    td {
    text-align: center;
    }
</style>
{% endblock %}

{% block content %}
  {# NOTE: one list to rule them all! (else we potentially generate the list) #}
  {% set sample_list = get_variable("syssamples") %}

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


  <h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','flexeval')}}" alt=">" /> {{get_variable("subtitle","Test")}} - step {{get_variable("step")}} over {{get_variable("max_steps")}}</h2>

  <form action="./save" method="post" enctype="multipart/form-data" class="form-example" id="the_form">

    <fieldset class="form-group">
      <legend class="col-form-label" style="font-size: large; background-color: #e8f4ea; color: #000; padding: 20px; margin-top: 20px; margin-bottom:20px; border-radius: 25px;">
        {% block instruction %}
          <strong>Question:</strong> How do you judge the <strong>quality</strong> of the following candidates against the reference?
        {% endblock %}
      </legend>

      <div class="form-group" style="margin-bottom:20px;">
        <center>
          <audio id="sample" controls>
            <source id="sample_src" src="">
            Your browser does not support the <code>audio</code> element.
          </audio>
        </center>
      </div>

      <div class="form-group" style="margin-bottom:20px;">
          <table width="100%">
              <tbody>
                  <tr>
                    <td><b>System</b></td>
                    <td><b><button type="button" class="btn btn-primary btn-mute" id="audio_{{sample_list|length}}" onclick="selectSample({{sample_list|length}})">Reference</button></b></td>
                    {% for syssample in sample_list%}
                      {% set name_field = get_variable("field_name", name="sample_%d" % loop.index, syssamples=[syssample]) %}
                      <td>
                        <button type="button" class="btn btn-primary btn-mute" id="audio_{{loop.index-1}}" onclick="selectSample({{loop.index - 1}})">Sample {{loop.index}}</button>
                      </td>
                    {% endfor %}
                  </tr>
                  <tr>
                      <td><b>Fully played?</b></td>
                      <td>
                        <img id="checked_{{sample_list|length}}" src="{{get_asset('img/checked.svg')}}" height="20px" style="display: none;" />
                      </td>
                      {% for syssample in sample_list %}
                      <td>
                          <img id="checked_{{loop.index-1}}" src="{{get_asset('img/checked.svg')}}" height="20px" style="display: none;" />
                      </td>
                      {% endfor %}
                  </tr>
                  <tr>
                    <td><b>Rank</b></td>
                    <td></td>
                    {% for syssample in sample_list %}
                      {% set name_field = get_variable("field_name",name="rank_score_%d" % loop.index, syssamples=[syssample]) %}
                      <td class="slider-container">
                        <input type="range" id="score_{{loop.index}}" name="{{ name_field }}" class="form-control-range" data-trigger="hover" data-vertical="true" data-toggle="popover" data-content="Fair (50)" data-slider-min="0" data-slider-max="100" data-slider-step="1" data-slider-value="50" required />
                      </td>
                    {% endfor %}
                  </tr>
              </tbody>
          </table>
      </div>

      <center>
        <button type="submit" id="submit" class="btn btn-primary" title="You haven't played all the samples yet">Submit</button>
      </center>
  </form>

  <script>
    {% set sysref_sample = get_variable("syssamples", get_variable("sysref"))[0] %}
    {% set sysref_content, sysref_mimetype = sysref_sample.get(num=0) %}

      const list_audios = [
          {% for syssample in sample_list %}
          {% set content,mimetype = syssample.get(num=0)  %}
          {% if mimetype.startswith("audio") %}
          ["{{syssample}}", "{{content}}"],
          {% endif %}
        {% endfor %}
        {% if sysref_mimetype.startswith("audio") %}
          ["{{sysref_sample}}", "{{sysref_content}}"]
          {% endif %}

      ];


      var audio = document.getElementById("sample");
      var audio_source = document.getElementById("sample_src");
      var cur_sample_index = -1;
      var cur_selected_audio_btn = null;

      const URL_MONITOR =  window.location.href + "monitor";
      const monitor_handler = async (action, value, sample_id) => {
          const body = {
              "sample_id": sample_id,
              "info_type": action,
              "info_value": value
          }
          // FIXME: the URL needs to be generalised (both base part & stage part)
          const response = await fetch(URL_MONITOR, {
              method: 'POST',
              body: JSON.stringify(body),
              headers: {
                  'Content-Type': 'application/json'
              }
          });
      }

      audio.onpause = function() {
          if (audio.currentTime < audio.duration) {
              monitor_handler("pause", audio.currentTime, list_audios[cur_sample_index][0]);
          } else {
              monitor_handler("ended", audio.currentTime, list_audios[cur_sample_index][0]);
          }
      };

      audio.onplay = function() {
          monitor_handler("play", audio.currentTime, list_audios[cur_sample_index][0]);
      };


      function selectSample(index) {
          if (cur_sample_index >= 0) {
              monitor_handler("switch_sample", ["sampleid:" + list_audios[index][0], audio.duration], list_audios[cur_sample_index][0]);
          }

          audio_source.src = list_audios[index][1];
          audio.load();
          cur_sample_index = index;


          // Update button to reflect the new status
          if (cur_selected_audio_btn) {
              cur_selected_audio_btn.disabled = false;
              cur_selected_audio_btn.classList.replace("btn-solo", "btn-mute");
          }

          cur_selected_audio_btn = document.getElementById("audio_" + index);
          cur_selected_audio_btn.disabled = true;
          cur_selected_audio_btn.classList.replace("btn-mute", "btn-solo");
          audio.play()
      }


      function validateForm() {
          for (let i = 1; i <= 5; i++) {
              let scoreValue = document.getElementById('score_' + i).value;
              if (scoreValue == '1') {
                  return true;
              }
          }
          showOverlay();
          return false;
      }

      function showOverlay() {
          document.getElementById('overlay').style.display = 'block';
      }

      function closeOverlay() {
          document.getElementById('overlay').style.display = 'none';
      }

      document.getElementById('the_form').onsubmit = function() {
          return validateForm();
      };

      var played_audios = new Set();

      audio.onended = function() {
          played_audios.add(audio_source.src);

          // Enable the submit button if all audios have been played
          if (played_audios.size === list_audios.length) {
              document.getElementById('submit').disabled = false;
          }

          // Show the fact that sample is
          var checked = document.getElementById("checked_" + cur_sample_index);
          checked.style.display = "";
      };
      // Initially disable the submit button
      document.getElementById('submit').disabled = true;
  </script>
{% endblock %}
