<%inherit file="/layout.mako" />
<%namespace file="../accounts/func.mako" import="password_reset"/>
<%def name="title()">Activate your account</%def>

${password_reset(user, reset=True)}
