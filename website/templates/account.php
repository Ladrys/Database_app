<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="icon" href="favicon.ico" type="image/x-icon">
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
    integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous" />
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
    crossorigin="anonymous" />

  <title></title>
</head>

<body>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">My E-shop</a>
   
    <form class="form-inline my-2 my-lg-0" action="/search" method="GET">
      <input class="form-control form-control-sm mr-sm-2 rounded-pill" type="search" placeholder="Search" aria-label="Search" name="q">
      <button class="btn btn-outline-success btn-sm rounded-pill" type="submit">Search</button>
    </form>
    
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
      aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav mr-auto">
      
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('views.home') }}">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('views.products') }}">Products</a>
        </li>
      </ul>

      
      
      <ul class="navbar-nav ml-auto">

        <li class="nav-item">
            <a class="nav-link" href="{{ url_for('views.cart') }}">Cart</a>
          </li>
          {% if 'username' in session %}
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('auth.account') }}">{{ session['username'] }}</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('auth.logout') }}">Logout</a>
        </li>
      </ul>
      {% else %}
      <ul class="navbar-nav ml-auto">
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('auth.login') }}">Log in</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('auth.register') }}">Sign-up</a>
        </li>
      </ul>
      {% endif %}
    </div>
  </nav>
   
  <div class="container my-5">
  <h1 class="text-center mb-5">Account Information</h1>
  <div class="row justify-content-center">
    <div class="col-md-6">
    <form method="POST" action="{{ url_for('views.order_history') }}">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" class="form-control" id="name" value="{{ session['username'] }}" readonly>
        </div>
        <div class="form-group">
          <label for="city">City:</label>
          <input type="text" class="form-control" id="city" name="city" value="{{ city }}">
        </div>
        <div class="form-group">
          <label for="credit">Credit Points:</label>
          <input type="text" class="form-control" id="credit" value="{{ credit_points }}" readonly>
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" class="form-control" id="email" name="email" value="{{ email }}">
        </div>
        <div class="form-group">
          <label for="telephone">Telephone:</label>
          <input type="telephone" class="form-control" id="telephone" name="telephone" value="{{ telephone }}">
        </div>
        <button type="submit" class="btn btn-primary">Save Changes</button>
        <a href="{{ url_for('views.order_history') }}" class="btn btn-secondary">Order History</a>

      </form>
    </div>
  </div>
</div>

  
  <script src="script.js"></script> 
  
</body>
</html>
