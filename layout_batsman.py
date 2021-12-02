html_layout = """ <html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Dash Board</title>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
  <style>
  /**
 * index.scss
 * - Add any styles you want here!
 */

 body {
    background: #2d2d7f !important;
    color: #fff;
  }
  /* main-header start */
  [data-target="#mainMenu"] {
    position: relative;
    z-index: 999;
  }
  .dash-dropdown{
      color:#000;
  }
  .desc_text{
    color: #fff;
    font-size: 20px;
    padding-top: 5px;
    padding-bottom: 15px;
    
  }
  #mainMenu li > a {
    font-size: 12px;
    letter-spacing: 1px;
    color: #fff;
    font-weight: 400;
    position: relative;
    z-index: 1;
    text-decoration: none;
  }
  
   .componet_text{
    color: #fff;
    font-size: 20px;
    text-align: center;
    padding-top: 15px;
    padding-bottom: 5px;
    font-weight: bold;

  }
  .h3_head{
    text-align: center;
    padding-top: 30px;
    margin-bottom: -5px;
  }
  .main-header.fixed-nav #mainMenu li > a {
    color: #fff;
    text-decoration: none;
  }
  
  #mainMenu li:not(:last-of-type) {
    margin-right: 30px;
  }
  
  #mainMenu li > a::before {
    position: absolute;
    content: "";
    width: calc(100% - 1px);
    height: 1px;
    background: #fff;
    bottom: -6px;
    left: 0;
  
    -webkit-transform: scale(0, 1);
    -ms-transform: scale(0, 1);
    transform: scale(0, 1);
    -webkit-transform-origin: right center;
    -ms-transform-origin: right center;
    transform-origin: right center;
    z-index: -1;
  
    -webkit-transition: transform 0.5s ease;
    transition: transform 0.5s ease;
  }
  
  #mainMenu li > a:hover::before,
  #mainMenu li > a.active::before {
    -webkit-transform: scale(1, 1);
    -ms-transform: scale(1, 1);
    transform: scale(1, 1);
    -webkit-transform-origin: left center;
    -ms-transform-origin: left center;
    transform-origin: left center;
  }
  
  .main-header.fixed-nav #mainMenu li > a::before {
    background: #000;
  }
  
  .main-header {
    position: fixed;
    top: 0px;
    background-color: #2d2d7f;
    padding-top: 25px;
    padding-bottom: 15px;
    left: 0;
    z-index: 99;
    width: 100%;
    -webkit-transition: all 0.4s ease;
    transition: all 0.4s ease;
  }
  
  .main-header.fixed-nav {
    top: 0;
    background: #fff;
    -webkit-box-shadow: 0 8px 12px -8px rgba(0, 0, 0, 0.09);
    box-shadow: 0 8px 12px -8px rgba(0, 0, 0, 0.09);
    -webkit-transition: all 0.4s ease;
    transition: all 0.4s ease;
  }
  
  .main-header.fixed-nav .navbar-brand > img:last-of-type {
    display: block;
  }
  
  .main-header.fixed-nav .navbar-brand > img:first-of-type {
    display: none;
  }
  .navbar-brand {
    color: #fff;
  }
  .main-header .navbar-brand img {
    max-width: 40px;
    animation: fadeInLeft 0.4s both 0.4s;
  }
  /* main-header end */
  @media (max-width: 991px) {
    /*header starts*/
  
    .collapse.in {
      display: block !important;
      padding: 0;
      clear: both;
    }
  
    .navbar-toggler {
      margin: 0;
      padding: 0;
      width: 40px;
      height: 40px;
      position: absolute;
      top: 25px;
      right: 0;
      border: none;
      border-radius: 0;
      outline: none !important;
    }
  
    .main-header .navbar {
      float: none;
      width: 100%;
      padding-left: 0;
      padding-right: 0;
      text-align: center;
    }
  
    .main-header .navbar-nav {
      margin-top: 70px;
    }
  
    .main-header .navbar-nav li .nav-link {
      text-align: center;
      padding: 20px 15px;
      border-radius: 0px;
    }
    /**/
    .main-header .navbar-toggler .icon-bar {
      background-color: #fff;
      margin: 0 auto 6px;
      border-radius: 0;
      width: 30px;
      height: 3px;
      position: absolute;
      right: 0;
      -webkit-transition: all 0.2s ease;
      transition: all 0.2s ease;
    }
  
    .main-header .navbar .navbar-toggler .icon-bar:first-child {
      margin-top: 3px;
    }
  
    .main-header .navbar-toggler .icon-bar-1 {
      width: 10px;
      top: 0px;
    }
  
    .main-header .navbar-toggler .icon-bar-2 {
      width: 16px;
      top: 12px;
    }
  
    .main-header .navbar-toggler .icon-bar-3 {
      width: 20px;
      top: 21px;
    }
  
    .main-header .current .icon-bar {
      margin-bottom: 5px;
      border-radius: 0;
      display: block;
    }
  
    .main-header .current .icon-bar-1 {
      width: 18px;
    }
  
    .main-header .current .icon-bar-2 {
      width: 30px;
    }
  
    .main-header .current .icon-bar-3 {
      width: 10px;
    }
  
    .main-header .navbar-toggler:hover .icon-bar {
      background-color: #fff;
    }
  
    .main-header .navbar-toggler:focus .icon-bar {
      background-color: #fff;
    }
  
    /*header ends*/
  }
  
  </style>
</head>

<body>
  <header class="main-header">
    <div class="container">
      <nav class="navbar navbar-expand-lg main-nav px-0">
        <div class="collapse navbar-collapse justify-content-center" id="mainMenu">
          <ul class="navbar-nav text-uppercase f1">
            <li>
              <a href="/dashboard/">home</a>
            </li>
            <li>
              <a href="/batsmen" class="active active-first">batsmen</a>
            </li>
            <li>
              <a href="/bowler">bowlers</a>
            </li>
            <li>
              <a href="/logout">logout</a>
            </li>
          </ul>
        </div>
      </nav>
    </div>
    <!-- /.container -->
  </header>
  <div class="container">
        <h1 class="text-center" style="margin-top: 100px;color: #fff;"> Batsmens Visualizations</h1>
    </div>
  <div class="container">
                {%app_entry%}
    </div>
<footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
  <!-- Scripts -->
  <script src="scripts/index.js"></script>

</body>

</html>
  """
