{% extends get_template('base.tpl') %}

{% block head %}
  <style>

    .word, .boundary {
    display: inline-block;
    margin-right: 5px;
    padding: 5px 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: #f4f4f4;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
    }

    .word:hover, .boundary:hover {
    background-color: #d1ecf1;
    transform: scale(1.1);
    }

    .selected {
    background-color: #f8d7da; /* Pastel red */
    border-color: #f5c2c7;
    }
  </style>
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
        {% set content, mimetype = syssample.get('audio')  %}

        <div id="player_area">
          <center>
            {% block player_view scoped %}
              {% include get_template('players/default/player.html') %}
            {% endblock %}
          </center>
        </div>

        {# Rapid Prosody Transcription Part #}
        <div id="rpt_area">
          <div id="text-container"></div>
          <input type="hidden" id="selected-items" name="selected_items" value="">
        </div>

        {# MOS Part #}
        <div id="mos_area">
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
      </div>
    </fieldset>

    <button type="submit" id="submit" class="btn btn-primary">Submit</button>
  </form>

  <script>
    {% block player_controls scoped %}
      {% include get_template('players/default/controls.js') %}
    {% endblock %}

    //
    {% set text_content, ignored = syssample.get('text') %}
    const text = '{{text_content}}';
    const selectedItems = [];
    const textContainer = document.getElementById("text-container");
    const selectedItemsField = document.getElementById("selected-items");

    function updateSelectedList() {
    	// Sort by original index to maintain presentation order
    	selectedItems.sort((a, b) => a.index - b.index);
    	selectedItemsField.value = selectedItems.map(({ item }) => item).join(",");
    }

    // Function to toggle selection and maintain original order
    function toggleSelection(element, item, index) {
    	const existingIndex = selectedItems.findIndex(el => el.item === item);
    	if (existingIndex > -1) {
            // If already selected, remove it
    	    selectedItems.splice(existingIndex, 1);
    	    element.classList.remove("selected");
    	} else {
            // Otherwise, add it with the original index
            selectedItems.push({ item, index });
            element.classList.add("selected");
        }

        updateSelectedList();
    }

    // Split text into words and boundaries
    const regex = /([\w'-]+|[.,!?])/g; // Match words or boundaries
    const matches = text.match(regex);

    matches.forEach((match, index) => {
        const element = document.createElement("span");
        element.textContent = match;
        element.className = /[.,!?]/.test(match) ? "boundary" : "word"; // Boundary or word class
        element.onclick = () => toggleSelection(element, match, index); // Pass index
        textContainer.appendChild(element);
    });
  </script>
{% endblock %}
