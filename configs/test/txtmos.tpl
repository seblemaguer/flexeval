<html>

  <head>
    <title> Test MOS </title>
  </head>

  <body>

    <form action="./{{name}}/send" method="post" class="form-example">

      {% for system in systems %}
        <p> Blabla: {{system.json["sentence1"]}},{{system.json["sentence2"]}} </p>
        <select name="{{ system.save_field('score') }}">
         <option value="1">Médiocre</option>
         <option value="2">Moyen</option>
         <option value="3">Correct</option>
         <option value="4"> Bon </option>
        </select>
      {% endfor %}

      <button>Send</button>

    </form>

  </body>

</html>
