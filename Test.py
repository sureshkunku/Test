<!DOCTYPE html>
<html lang="en">
{% load static %}

<head>
    <meta charset="UTF-8">
    <link rel="stylesheet"
    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
    <script
    src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script
    src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script
    src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
    <link href="https://cdn.jsdelivr.net/gh/gitbrent/bootstrap4-toggle@3.6.1/css/bootstrap4-toggle.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/gh/gitbrent/bootstrap4-toggle@3.6.1/js/bootstrap4-toggle.min.js"></script>
    <title>Email Sender</title>
    <script src="//cdn.ckeditor.com/4.14.1/standard/ckeditor.js"></script>
    <style>
        .logocontainer img {
                float:left;
                margin-left:10px;
                height: 25px;
        }
        .headertitle {
                text-align:right;
                float:right;
                margin-right:10px;
                color: white;
                width:300px;
        }
        .menubar {
            background-color:#002b51;
            padding-top: 10px;
            padding-bottom: 10px;
        }
        .form-group{
            padding-top:20px;
        }
        .click_button {
          background-color: #002b51;
          border: none;
          color: white;
          padding: 10px 10px;
          text-align: center;
          text-decoration: none;
          display: inline-block;
          font-size: 16px;
          border-radius: 12px;
        }
        .footer {
           position: fixed;
           left: 0;
           bottom: 0;
           width: 100%;
           background-color: #002b51;
           color: white;
           text-align: center;
        }
        .message {
            border-radius: 10px;
            box-shadow: 3px 3px 4px 0px rgba(50, 50, 50, 0.75);
            <!--color: white;-->
            margin-bottom: 20px;
            margin-left: auto;
            margin-right: auto;
            padding-bottom: 5px;
            padding-top: 5px;
            text-align: center;
            width: 80%;
        }
        .message.success {
            background-color: green;
        }

        .message.error {
            background-color: red;
        }
        .first_col {
            -ms-flex: 0 0 230px;
            flex: 0 0 250px;
        }
        <!--.send_button {-->
           <!--background-color: #002b51;-->
           <!--color: white;-->
           <!--text-align: center;-->
           <!--border-radius: 8px;-->
           <!--padding: 20 px;-->
        <!--}-->
    </style>

</head>
<body>
    <div class="menubar">
        <div class="row">
            <div class="col-2">
                <div class="logocontainer">
                    <a href="/">
                        {% load static %}
                        <img src="{% static 'qualtrics_webapp/logo-white.png' %}" alt="gartner image">
                    </a>
                </div>
            </div>
            <div class="col">
            </div>
            <div class="col-2">
                <div class="headertitle">Email sender
                </div>
            </div>
          </div>
    </div>
    {% block messages %}
        <ul class="messages" id="messages-list">
        {% if messages %}
            {% for message in messages %}
            <li>
                {% if message.tags %}
                     <div class="alert alert-{{ message.tags }} msg fade show" role="alert">{{ message }}</div>
                {% else %}
                    <div class="alert alert-info msg fade show" role="alert">{{ message }}</div>
                {% endif %}
            </li>
            {% endfor %}
        {% endif %}
        </ul>
        {% endblock %}

        {% block scripts %}
            <script src="{% static 'journal/scripts/main.js' %}"></script>
        {% endblock %}
    <form action="{% url 'excel_data' %}" method="post" enctype="multipart/form-data">
        {% csrf_token %}
    <div class="container px-5 py-24 mx-auto">
        <div class="flex flex-wrap -m-12">
            <div class="p-12 md:w-1/2 flex flex-col items-start">
                <div class="row">
                    <div class="col first_col">
                        <label for="subject" style="font-weight:bold">Qualtrics Survey Links Excel :</label>
                    </div>
                    <div class="col-8">
                        <input type="file"  multiple="multiple"
                               title="Upload qualtrics excel file"
                               name="qual_excel_file"
                               style="border: 1px solid black; padding: 1px;"
                               required="required"
                                >
                    </div>
                </div>
                <div class="row">
                    <div class="col first_col">
                        <label for="subject" style="font-weight:bold">GRB Contact List Excel :</label>
                    </div>
                    <div class="col-8">
                        <input type="file"
                               title="Upload DS excel file"
                               name="ds_excel_file"
                               style="border: 1px solid black; padding: 1px;"
                               required="required"
                                >
                    </div>
                </div>
                <div class="row">
                    <div class="col first_col">
                        <label for="board" style="font-weight:bold">Choose a Primary Board:</label>
                    </div>

                    <div class="col-8">
                        <select name="board" id="board">
                          <option value="GCIO">GCIO</option>
                          <option value="GCIO CTBM">GCIO CTBM</option>
                          <option value="RCIO">RCIO</option>
                          <option value="RCIO CTBM">RCIO CTBM</option>
                            <option value="DARB">DARB</option>
                          <option value="DARB CTBM">DARB CTBM</option>
                          <option value="FMRB">FMRB</option>
                          <option value="FMRB CTBM">FMRB CTBM</option>
                            <option value="IRMRB">IRMRB</option>
                          <option value="IRMRB CTBM">IRMRB CTBM</option>
                            <option value="SSRB">SSRB</option>
                          <option value="SSRB CTBM">SSRB CTBM</option>
                            <option value="TIRB">TIRB</option>
                          <option value="TIRB CTBM">TIRB CTBM</option>
                          <option value="WMRB">WMRB</option>
                          <option value="WMRB CTBM">WMRB CTBM</option>
                            <option value="Other1">Other1</option>
                          <option value="Other2">Other2</option>
                            <option value="Other3">Other3</option>
                            <option value="Other4">Other4</option>
                        </select>
                    </div>
                </div>
                <div class="row">
                    <div class="col first_col">
                        <label for="sec_board" style="font-weight:bold">Choose a Secondary Board:</label>
                    </div>

                    <div class="col-8">
                        <select name="sec_board" id="sec_board" multiple>
                          <option value="GCIO">GCIO</option>
                          <option value="GCIO CTBM">GCIO CTBM</option>
                          <option value="RCIO">RCIO</option>
                          <option value="RCIO CTBM">RCIO CTBM</option>
                            <option value="DARB">DARB</option>
                          <option value="DARB CTBM">DARB CTBM</option>
                          <option value="FMRB">FMRB</option>
                          <option value="FMRB CTBM">FMRB CTBM</option>
                            <option value="IRMRB">IRMRB</option>
                          <option value="IRMRB CTBM">IRMRB CTBM</option>
                            <option value="SSRB">SSRB</option>
                          <option value="SSRB CTBM">SSRB CTBM</option>
                            <option value="TIRB">TIRB</option>
                          <option value="TIRB CTBM">TIRB CTBM</option>
                          <option value="WMRB">WMRB</option>
                          <option value="WMRB CTBM">WMRB CTBM</option>
                            <option value="Other1">Other1</option>
                          <option value="Other2">Other2</option>
                            <option value="Other3">Other3</option>
                            <option value="Other4">Other4</option>


                        </select>
                    </div>
                </div>
                <div class="row">
                    <div class="col first_col">
                        <label for="from_send" style="font-weight:bold">FROM :</label>
                        <!--<label for="subject" style="background-color: #2196F3;">Subject :</label>-->
                    </div>
                    <div class="col-8">

                        <select name="from_send" id="from_send">
                            <option value="rb.consulttheboard@gartner.com">rb.consulttheboard@gartner.com</option>
                            <option value="rcrb.consulttheboard@gartner.com">rcrb.consulttheboard@gartner.com</option>
                            <option value="darbconsulttheboard@gartner.com">darbconsulttheboard@gartner.com</option>
                            <option value="fmrb.consulttheboard@gartner.com">fmrb.consulttheboard@gartner.com</option>
                            <option value="irmrb.consulttheboard@gartner.com">irmrb.consulttheboard@gartner.com</option>
                            <option value="ssrb.consulttheboard@gartner.com">ssrb.consulttheboard@gartner.com</option>
                            <option value="tirb.consulttheboard@gartner.com">tirb.consulttheboard@gartner.com</option>
                            <option value="wmrb.consulttheboard@gartner.com">wmrb.consulttheboard@gartner.com</option>
                            <option value="siobhan.obrien@gartner.com">siobhan.obrien@gartner.com</option>
                            <option value="kunkusuresh.babu@labgartner.com">kunkusuresh.babu@labgartner.com</option>
                        </select>
                    </div>
                </div>
                <div class="row">
                    <div class="col first_col">
                        <label for="subject" style="font-weight:bold">Subject :</label>
                        <!--<label for="subject" style="background-color: #2196F3;">Subject :</label>-->
                    </div>
                    <div class="col-8">
                        <textarea id="subject" name="subject" rows="1" cols="80">  Subject</textarea>
                    </div>
                </div>

                <div class="row">
                    <div class="col first_col">
                        <label for="email_body" style="font-weight:bold">Email Body :</label>
                    </div>
                    <div class="col-8">
                        <!--{% csrf_token %}-->
                        <textarea id="email_body" name="email_body" rows="10" cols="80">  Please enter the email body.</textarea>
                        <script>
                            CKEDITOR.replace( 'email_body' );
                        </script>
                    </div>
                </div>

                <div class="row">
                    <div class="col first_col">

                    </div>
                    <div class="col text-left">

                    <div class="row">
                    <div class="col first_col">
                        <label for="subject" style="font-weight:bold">Email attachments :</label>
                    </div>
                    <div class="col-8">
                        <input type="file"  multiple="multiple"
                               title="Upload email attachments files"
                               name="email_attachment_files"
                               style="border: 1px solid black; padding: 1px;"
                        >
                    </div>
                    <div class="col first_col">
                        <label for="subject" style="font-weight:bold">Select Template :</label>
                    </div>
                </div>
                <input type="radio" name="template" value="Standard">Standard survey<br>
                <input type="radio" name="template" value="Summary">Summary announcement<br>
                <input type="radio" name="template" value="Blank">Blank template<br>

                <div class="form-check pl-0">
                  <input type="checkbox" name="toggle" value="on" checked="true" data-toggle="toggle"> Auto Sent Email
                </div>
                    <input class="send_button" type="submit"
                   value="Send Email"
                   style="background-color: #002b51; color: white; text-align: center;
                            padding-left:20px; padding-right:20px; padding-top:10px;
                            padding-bottom:10px; border-radius: 8px; cursor: pointer;">

                    </div>
                </div>
            </div>
        </div>
    </div>
    </form>
    <div class="footer">
        <div class="col-md-12">
            <div class="copy-right text-center">© 2022 Gartner, Inc. and/or its Affiliates. All Rights Reserved.
            </div>
        </div>
    </div>
</body>
</html>
