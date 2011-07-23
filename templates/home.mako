<%inherit file="base.mako"/>

<%namespace name="utils" file="utils.mako"/>

<%block name="title">Home</%block>


<h1>Welcome home !</h1>


<h2>Profile details</h2>

${utils.render_as_list(me)}


<h2>My contacts</h2>

<ul>
    %for c in contacts:
        <li>${c.get('name')}</li>
    %endfor
</ul>

