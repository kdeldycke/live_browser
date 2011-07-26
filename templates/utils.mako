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
                    <li><span class="label">${render_id(k)}</span>: ${render_as_list(v)}</li>
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


<%def name="remove_cruft(data)">
    ## Simplify the data structure by recursively removing Nones, empty strings, empty lists and dicts.
    ## This utility also transforms one-item lists to the only item they contain.
    <%
        if type(data) is type([]):
            cleaned_list = [remove_cruft(i) for i in data if i]
            cleaned_list = [i for i in cleaned_list if i]
            if len(cleaned_list) == 1:
                return cleaned_list.pop()
            return cleaned_list
        elif type(data) is type({}):
            cleaned_dict = dict([(k, remove_cruft(v)) for (k, v) in data.items() if v])
            return dict([(k, v) for (k, v) in cleaned_dict.items() if v])
        elif data:
            return data
        return None
    %>
</%def>


<%def name="render_error(error)">
    <%
        error = error['error']
    %>
    <p class='error'>${error['message']} (code: <code>${error['code']}</code>)</p>
</%def>

