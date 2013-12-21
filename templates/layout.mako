# -*- coding: utf-8 -*- 
<!DOCTYPE html>  
<!--[if IE 9]><html class="lt-ie10" lang="en" > <![endif]-->
<html class="no-js" lang="en" >
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>app</title>

    <!-- If you are using CSS version, only link these 2 files, you may add app.css to use for your overrides if you like. -->
    <link rel="stylesheet" href="/static/css/normalize.css">
    <link rel="stylesheet" href="/static/css/foundation.css">
    <script src="/static/js/vendor/custom.modernizr.js"></script>
</head>

<body>

  <div id="page">
    
    ${next.body()}

  </div>

  <script src="/static/js/vendor/jquery.js"></script>
  <script src="/static/js/foundation.min.js"></script>
  <script>
    $(document).foundation();
  </script>
</body>
</html>
