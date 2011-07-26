<%inherit file="base.mako"/>

<%namespace name="utils" file="utils.mako"/>

<%block name="title">Home</%block>


<h1>${profile_info.get('name')}'s profile</h1>


<h2>Details</h2>

## Pagination code taken from https://github.com/gbirke/jquery_pagination/blob/master/src/demo/demo.htm
<div id="Searchresult">
    This content will be replaced when pagination inits.
</div>
<div id="hiddenresult" class="hidden">
    <%
        # Pagination function inspired by http://stackoverflow.com/questions/3744451/is-this-how-you-paginate-or-is-there-a-better-algorithm/3744524#3744524
        def paginate(d, lenght):
            seq = d.items()
            for start in xrange(0, len(seq), lenght):
                yield dict(seq[start:start+lenght])
    %>
    %for page_content in paginate(utils.remove_cruft(profile_info), 5):
        <div class="result">
            ${utils.render_as_list(page_content)}
        </div>
    %endfor
</div>
<div id="Pagination" class="pagination clearfix"></div>


<h2>Contacts</h2>

%if 'error' in contacts:
    ${utils.render_error(contacts)}
%else:
    <ul>
        %for c in contacts:
            <li><a href="/profile/${c.get('user_id')}">${c.get('name')}</a></li>
        %endfor
    </ul>
%endif

