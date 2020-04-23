{% extends get_template('base.tpl','perceval') %}

{% set gdpr = get_variable("GDPR")%}
{% block content %}
<h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> Legal Terms  </h2>

<h3 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> Privacy Policy</h3>

<p>
  This privacy policy, will explain, how your personal data that we collect from you when you use our website are used.
</p>

<span>Topics</span>
<ul>

  <li>Who we are?</li>
  <li>What data we collect?</li>
  <li> How do we collect your data?</li>
  <li>How will we use your data?</li>
  <li>How do we store your data?</li>
  <li>What are your data protection rights?</li>
  <li>What are cookies?</li>
  <li>How do we use cookies?</li>
  <li>What types of cookies do we use?</li>
  <li>How to manage your cookies?</li>
  <li>Privacy policies of other websites.</li>
  <li>How to contact us?</li>
  <li>How to contact the appropriate authority?</li>
</ul>

<h4 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> Who we are?</h4>
<p>
  The data are gathered in the name of {{gdpr["data_controller"]["identity"]}}.
  That you can contact by the following means:
  <ul>
    {%if gdpr["data_controller"]["contact"]["email"] is not none%}<li>{{gdpr["data_controller"]["contact"]["email"]}}</li>{% endif %}
    {%if gdpr["data_controller"]["contact"]["other"] is not none%}<li>{{gdpr["data_controller"]["contact"]["other"]}}</li>{% endif %}
  </ul>

  {% if len(gdpr["data_collection"]["recipients"]) > 0 %}
  The data can be communicate to the following recipients:
  <ul>
    {% for recipient in gdpr["data_collection"]["recipients"]%}
    <li>{{recipient}}</li>
    {% endfor %}
  </ul>

  {% endif %}
</p>

<h4 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> What data we collect?</h4>
<p>
We collect the following data:
<ul>
  {% for data in gdpr["data_collection"]["data"]%}
  <li>{{data}}</li>
  {% endfor %}
</ul>
</p>

<h4 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> How do we collect your data?</h4>
<p>
  You directly provide most of the data we collect. We collect data and process data when you:
  <ul>
    <li> Register online, </li>
    <li> Voluntarily complete a survey, </li>
    <li> Use or view our website via your browser’s cookies. </li>
  </ul>

  We may also receive your data indirectly from the following sources:
  <ul>
    <li>If someone enter your email into this website in order to send you an invitation to join this website.</li>
    <li>If someone enter your email instead of it's own email.</li>
  </ul>
</p>

<h4 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> How will we use your data?</h4>
<p>
  {{gdpr["data_collection"]["purpose"]}}
</p>

<h4 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> How do we store your data?</h4>
<p>
  Your data is securely store.
  {% if gdpr["data_conservation"]["security_measures"] is not none %}
    {{gdpr["data_conservation"]["security_measures"]}}
  {% endif %}

  {% if gdpr["data_conservation"]["duration"] is not none %}
    Your data will be keep during: {{gdpr["data_conservation"]["duration"]}}.
  {% endif %}

  {% if gdpr["data_conservation"]["criterions_duration"] is not none %}
    Your data will be keep until: {{gdpr["data_conservation"]["criterions_duration"]}}
  {% endif %}
</p>

<h4 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> What are your data protection rights?</h4>
<p>
  We would like to make sure you are fully aware of all of your data protection rights.
  Every user is entitled to the following:
  <ul>
    <li>The right to access - You have the right to request Our Company for copies of your personal data.
      We may charge you a small fee for, this service.</li>
    <li> The right to rectification - You have the right to request that we correct any, information you believe is inaccurate.
      You also have the right to request us to complete information you believe is incomplete.
    </li>

    <li>The right to erasure — You have the right to request that we erase your personal data, under certain conditions.
    </li>

    <li>The right to restrict processing - You have the right to request that we restrict the
  processing of your personal data, under certain conditions.</li>

    <li>The right to object to processing - You, have the right to object to our processing,
  of your personal data, under certain conditions.</li>

    <li>The right to data portability - You have the right to request that we transfer the
  data that we have collected to another organization, or directly to you, under certain conditions.
  </li>

  </ul>

  If you make a request, we have one month to respond to you.
  If you would,like to exercise any of these rights, use one of the following methods:

  {% if gdpr["data_protection_officer"]["contact"]["email"] is not none%}
  <li>Email,us at: {{gdpr["data_protection_officer"]["contact"]["email"]}}</li>
  {% endif %}

  {% if gdpr["data_protection_officer"]["contact"]["phone_number"] is not none%}
  <li>Call,us: {{gdpr["data_protection_officer"]["contact"]["phone_number"]}}</li>
  {% endif %}

  {% if gdpr["data_protection_officer"]["contact"]["other"] is not none%}
  <li>Or: {{gdpr["data_protection_officer"]["contact"]["other"]}}</li>
  {% endif %}

</p>

<h4 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> What are cookies?</h4>
<p>
  Cookies are text files placed on your computer to collect standard,,Internet log information and,
  visitor behavior information. When you visit our websites, we may collect,information from you,
  automatically through cookies or similar technology.
  For further information, visit <a href="aboutcookies.org">aboutcookies.org</a>.
</p>

<h4 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> How do we use cookies?</h4>
<p>
  We uses cookies in a range of ways to improve your experience on our website, including:
  <ul>
    <li>Keeping you signed in,</li>
    <li>Save some temporary variables link to our profile.</li>
  </ul>
</p>


<h4 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> What types of cookies do we use?</h4>
<p>
  There are a number of different types of cookies, however, our website uses:
  <ul>
    <li>Functionality — We uses these cookies so that we recognize you on our website
      and remember your previously selected preferences, and some technical information.
    </li>
  </ul>
</p>

<h4 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> How to manage your cookies?</h4>
<p>
  You can set your browser not to accept cookies, and the above website tells you, how to remove,
  cookies from your browser.
  However, our website may not function as a result.
</p>

<h4 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> Privacy policies of other websites.</h4>
<p>
  This website contains links to other websites. Our privacy policy applies only to, our website, so if you click on
  a link to another website, you should read their privacy policy.
</p>

<h4 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> How to contact us?</h4>
<p>
  If you have any questions about our privacy policy, the data we hold, on you, or you would,like to exercise one
  of your data protection, rights, please do not hesitate to contact us.
  <ul>
    {% if gdpr["data_protection_officer"]["contact"]["email"] is not none%}
    <li>Email,us at: {{gdpr["data_protection_officer"]["contact"]["email"]}}</li>
    {% endif %}

    {% if gdpr["data_protection_officer"]["contact"]["phone_number"] is not none%}
    <li>Call,us: {{gdpr["data_protection_officer"]["contact"]["phone_number"]}}</li>
    {% endif %}

    {% if gdpr["data_protection_officer"]["contact"]["other"] is not none%}
    <li>Or: {{gdpr["data_protection_officer"]["contact"]["other"]}}</li>
    {% endif %}

  </ul>
</p>

<h4 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> How to contact the appropriate authority?</h4>
Should you wish to report a complaint or if you feel that we has not addressed your concern in a satisfactory manner,
you may contact your local Information Commissioner’s Office: <a href="https://edpb.europa.eu/about-edpb/board/members_en">https://edpb.europa.eu/about-edpb/board/members_en</a>

</p>

<p>Source : <a href="https://gdpr.eu/privacy-notice/">https://gdpr.eu/privacy-notice/</a>

<h3 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','perceval')}}" alt=">" /> EULA</h3>
<p>
{{get_variable("EULA")["text"]}}
</p>


<a href="{{make_url('/')}}"> Back</a>

{% endblock %}
