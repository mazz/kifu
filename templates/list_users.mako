# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<h1>Users</h1>
<table>
    <thead>
        <tr>
            <td>Name</td>
            <td>Email</td>
            <td>Admin</td>
            <td>Activated</td>
        </tr>
    </thead>
    <tbody>

    % if users:
        % for user in users:
        <tr>
            <td>${user.username}</td>
            <td>${user.name}</td>
            <td>${user.is_admin}</td>
            <td>${user.activated}</td>
        </tr>
        % endfor
    % else:
        <tr>
            <td>No Users</td>
        </tr>
    % endif
    </tbody>
</table>

