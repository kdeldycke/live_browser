<%inherit file="base.mako"/>

<%block name="title">Login</%block>

<p>Welcome to Live Browser, a data snooping web application that will spy on you !</p>

<p>By connecting to this app, you allow us to collect all your personnal informations and let us store them indefinely.</p>

<p>All collected data will then be available to people connected to you by the contact social path.</p>

<p><a href="${auth_url}">Login with your Windows Live account</a></p>

<p class="error">This is a test project I created to explore the Windows Live API. It is not intended for public consumption.</p>
