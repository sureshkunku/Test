<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Sender</title>
    <!-- Add your custom stylesheets and fonts here -->
    <link rel="stylesheet" href="path/to/your/custom.css">
    <!-- Include Bootstrap 5 CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.7.0/dist/css/bootstrap.min.css">
</head>
<body>
    <header class="bg-primary text-white py-3">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-2">
                    <a href="/">
                        <img src="{% static 'qualtrics_webapp/logo-white.png' %}" alt="gartner image" height="25">
                    </a>
                </div>
                <div class="col-md-8 text-center">
                    <h1 class="h3">Email Sender</h1>
                </div>
                <div class="col-md-2 text-end">
                    <a href="#" class="btn btn-light">Login</a>
                </div>
            </div>
        </div>
    </header>

    <div class="container mt-5">
        {% block messages %}
            <!-- Messages block content here -->
        {% endblock %}
        
        <form action="{% url 'excel_data' %}" method="post" enctype="multipart/form-data">
            {% csrf_token %}
            <div class="row">
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="qual_excel_file" class="form-label">Qualtrics Survey Links Excel</label>
                        <input type="file" class="form-control" name="qual_excel_file" required>
                    </div>
                    <div class="mb-3">
                        <label for="ds_excel_file" class="form-label">GRB Contact List Excel</label>
                        <input type="file" class="form-control" name="ds_excel_file" required>
                    </div>
                    <div class="mb-3">
                        <label for="board" class="form-label">Choose a Primary Board</label>
                        <select class="form-select" name="board" id="board">
                            <!-- Primary board options here -->
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="sec_board" class="form-label">Choose a Secondary Board</label>
                        <select class="form-select" name="sec_board" id="sec_board" multiple>
                            <!-- Secondary board options here -->
                        </select>
                    </div>
                </div>
                <div class="col-md-6">
                    <!-- Other form fields here -->
                </div>
            </div>
            <button type="submit" class="btn btn-primary">Send Email</button>
        </form>
    </div>

    <footer class="bg-primary text-white py-3 fixed-bottom">
        <div class="container text-center">
            <p>&copy; 2022 Gartner, Inc. and/or its Affiliates. All Rights Reserved.</p>
        </div>
    </footer>

    <!-- Include Bootstrap 5 and other scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.7.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Add your custom JavaScript here -->
</body>
</html>
