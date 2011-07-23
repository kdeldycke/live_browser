<%inherit file="base.mako"/>

<%namespace name="utils" file="utils.mako"/>

<%block name="title">Home</%block>


<h1>Welcome home !</h1>


<h2>Profile details</h2>

## Pagination code taken from https://github.com/gbirke/jquery_pagination/blob/master/src/demo/demo.htm
<div id="Searchresult">
    This content will be replaced when pagination inits.
</div>
<div id="Pagination" class="pagination"></div>
<div id="hiddenresult" style="display:none;">
    <%
        # Pagination function inspired by http://stackoverflow.com/questions/3744451/is-this-how-you-paginate-or-is-there-a-better-algorithm/3744524#3744524
        def paginate(d, lenght):
            seq = d.items()
            for start in xrange(0, len(seq), lenght):
                yield dict(seq[start:start+lenght])
    %>
    %for page_content in paginate(me, 5):
        <div class="result">
            ${utils.render_as_list(page_content)}
        </div>
    %endfor
</div>


<h2>My contacts</h2>

<ul>
    %for c in contacts:
        <li>${c.get('name')}</li>
    %endfor
</ul>

