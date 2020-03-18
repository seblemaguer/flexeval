{% extends 'base.tpl' %}

{% block title %}ERREUR {{code}}{% endblock %}

{% block content %}

  <h1> Erreur {{code}} </h1>

  <p> Une erreur s'est produite </p>

  <a href="{{entrypoint}}"> Retour à l'accueil </a>

{% endblock %}

{% block footer %}
{% endblock %}
