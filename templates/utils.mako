<%def name="render_id(id_string)">
    %if id_string.startswith('_'):
        ## Print internal MongoDB data label as-is
        ${id_string}
    %else:
        ${id_string.title().replace('_', ' ')}
    %endif
</%def>

<%def name="render_as_list(data)">
    %if type(data) in [type([]), type({})]:
        <ul>
            %if type(data) is type({}):
                %for (k, v) in data.items():
                    <li>${render_id(k)}: ${render_as_list(v)}</li>
                %endfor
            %else:
                %for i in data:
                    <li>${render_as_list(i)}</li>
                %endfor
            %endif
        </ul>
    %elif type(data) in [type(''), type(u'')]:
        ${data}
    %else:
        ${repr(data)}
    %endif
</%def>

<%def name="render_error(error)">
    <%
        error = error['error']
    %>
    <p class='error'>${error['message']} (code: <code>${error['code']}</code>)</p>
</%def>

