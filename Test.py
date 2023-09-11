<body>
    <form id="myForm" action="your_upload_handler.php" method="POST" enctype="multipart/form-data">
        <label>
            <input type="radio" name="fileType" value="option1" id="option1"> Option 1 (Mandatory)
        </label>
        <label>
            <input type="radio" name="fileType" value="option2" id="option2"> Option 2 (Optional)
        </label>
        <br>
        <input type="file" name="file" id="fileInput" style="display: none;">
        <label for="fileInput" id="fileInputLabel" style="cursor: pointer;">Choose a File</label>
        <br>
        <input type="submit" value="Upload">
    </form>

    <script>
        const option1Radio = document.getElementById('option1');
        const fileInput = document.getElementById('fileInput');

        option1Radio.addEventListener('change', function () {
            if (option1Radio.checked) {
                fileInput.style.display = 'block';
                fileInput.required = true;
            } else {
                fileInput.style.display = 'none';
                fileInput.required = false;
            }
        });
    </script>
</body>
