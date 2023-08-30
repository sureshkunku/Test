import datetime
import logging
import time
import smtplib
import multiprocessing as mp
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from json import dumps
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from .constants import application_user_list, from_mail_ids, Email, DSExcel, QuaExcel, OutlookEmail, Access_Keys
from .emails_sender import MailSender, Token

log = logging.getLogger(__name__)


def index(request):
    """
    It will open the Login page of the application
    :param request:
    :return:  Json
    """
    template = loader.get_template('qualtrics_webapp/login.html')
    context = {
        'obj_list': ["sda", "das"],
    }

    return HttpResponse(template.render(context, request))


def health_check(request):
    """
    Health about the project
    :param request:
    :return:  Json
    """
    responseData = {
        "Response": "Application is running fine"
    }

    return JsonResponse(responseData)


def new(request):
    responseData = {
        "Response": "Application is running fine"
    }

    return JsonResponse(responseData)


def home(request):
    """
    It will validate the login credentials of the application
    :param request:
    :return: It will return the html pages based on validations
    """
    user = request.POST.getlist("email")[0]
    context = {
        'obj_list': ["sda", "das"],
    }

    if user in application_user_list:
        template = loader.get_template('qualtrics_webapp/home.html')
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('qualtrics_webapp/login.html')
        return HttpResponse(template.render(context, request))


def process_excel(request):
    """
    It will take the email compose as input and process the composer body and send to relevant folks to email
    :param request:   composer
    :return: Json
    """
    data = request.POST
    subject = data.get(Email.subject.value, "")
    mail_body = data.get(Email.mail_body.value, "")
    primary_board = data.get(Email.primary_board.value, "")
    secondary_board = data.getlist(Email.sec_board.value, [])
    from_send = data.get(Email.from_send.value, "")
    template = data.get(Email.template.value, "")

    if from_send.strip() in from_mail_ids:
        log.info(
            f"boards selected from_send:  {from_send}, primary_board : {primary_board}, secondary_board : {secondary_board}")
        ds_excel_file = request.FILES["ds_excel_file"]
        ds_wb = pd.read_excel(ds_excel_file)

        company_to_mail_dict, mail_id_to_board, mail_to_company_dict, message_list = read_ds_excel(ds_wb, primary_board,
                                                                                                   secondary_board)

        log.info(f"company_to_mail_dict : {company_to_mail_dict} and mail_to_company_dict : {mail_to_company_dict}")

        if len(subject.strip()) > 0 and len(mail_body.strip()) > 0:
            log.info("Both subject length and mail body length is not zero")
            qual_comp_id_dup_dict = {}
            mail_content = mail_body
            qual_excel_file = request.FILES.getlist("qual_excel_file")
            mail_list = []
            for excel in qual_excel_file:
                qual_excl = qual_excl_read(company_to_mail_dict, excel, from_send, mail_content, mail_id_to_board,
                                           mail_to_company_dict, primary_board, qual_comp_id_dup_dict, request,
                                           subject, template, mail_list)
                # if qual_excl:
                #     mail_list.append(qual_excl)

            start_time = time.time()
            log.info(f"Starting : {datetime.datetime.now()}")

            with ThreadPoolExecutor(max_workers=mp.cpu_count() - 1) as executor:
                result = executor.map(mail_sending, mail_list)

            for msg in result:
                message_list.append(msg)

            log.info(f"--- seconds ---  {(time.time() - start_time)}")
            log.info(f"Ending : {datetime.datetime.now()}")

            return render(request, 'qualtrics_webapp/mail_sender.html', {'data': dumps({"message_txt": message_list})})
        else:
            log.info("Either subject length is zero or mail body length is zero")
            return render(request, 'qualtrics_webapp/mail_sender.html',
                          {'data': dumps({"message_txt": "Please provide subject and mail body"})})
    else:
        log.info("Form Parameter is not set correctly")
        return render(request, 'qualtrics_webapp/mail_sender.html', {
            'data': dumps({"message_txt": "From parameter not entered correctly, go back to previous page"})})


def qual_excl_read(company_to_mail_dict, excel, from_send, mail_content, mail_id_to_board,
                   mail_to_company_dict, primary_board, qual_comp_id_dup_dict, request, subject,
                   template, mail_list):
    #mail_list = []
    wb = pd.read_excel(excel)
    for _, row in wb.iterrows():
        qual_mail_id = row[QuaExcel.email.value]
        if qual_mail_id in mail_to_company_dict:
            comp_id = mail_to_company_dict[qual_mail_id]
            qual_comp_id_dup_dict[comp_id] = False
            if comp_id in qual_comp_id_dup_dict:
                qual_comp_id_dup_dict[comp_id] = True

        log.info(f"qual_mail_id, {qual_mail_id}")
        mail_id__list = None
        if qual_mail_id in mail_to_company_dict:
            log.info("qual mail id found in mail_to_company_dict")
            comp_id = mail_to_company_dict[qual_mail_id]
            if qual_comp_id_dup_dict[comp_id] and mail_id_to_board[qual_mail_id] != primary_board:
                continue
            if comp_id in company_to_mail_dict:
                mail_id__list = company_to_mail_dict[comp_id]
        if mail_id__list is None:
            log.info(f"mail id list not found , {qual_mail_id}")
            continue
        log.info(f"mail_content : {mail_content}")
        links = []
        if row[QuaExcel.link.value] and template != "Blank":
            mail_content = mail_content + "<br>Begin the survey: <br><br>"
            links = [row.dropna().to_dict()]

        log.info(f"mail_id__list : {mail_id__list}")
        log.info(" ************************* sending using smtp **************************")
        mail = {"to_email": mail_id__list, "subject": subject, "mail_content": mail_content, "from_send": from_send,
                "files": request.FILES.getlist("email_attachment_files"),
                "links": links}
        flag = False
        for mail_check in mail_list:
            for inner_email in mail_id__list:
                if inner_email in mail_check["to_email"]:
                    flag = True
                    if template != "Blank":
                        mail_check["links"].append(row.dropna().to_dict())
                    break
        if not flag:
            mail_list.append(mail)

    return mail_list


def read_ds_excel(ds_wb, primary_board, secondary_board):
    """
     Read the DS excel
    :param ds_wb:
    :param primary_board:
    :param secondary_board:
    :return: return tuple of dicts
    """
    company_to_mail_dict = {}
    mail_to_company_dict = {}
    mail_id_to_board = {}
    message_list = []
    count = 0
    for _, row in ds_wb.iterrows():
        if count == 0:
            count = count + 1
            continue
        log.info(
            f" company:  {row[DSExcel.company.value]} , email : {row[DSExcel.email.value]}, board : {row[DSExcel.board.value]}")

        company_id = row[DSExcel.company.value]
        mail_id = row[DSExcel.email.value]
        board = row[DSExcel.board.value]
        doNotDistribute = row[DSExcel.doNotDistribute.value]
        if company_id and mail_id:
            if mail_id not in mail_to_company_dict:
                mail_to_company_dict[mail_id] = company_id
            if company_id not in mail_id_to_board:
                mail_id_to_board[mail_id] = board

        if str(doNotDistribute) != 'nan' and str(doNotDistribute).lower() == 'yes':
            log.info(f"BLACK LIST : {board} ")
            continue

        if len(secondary_board) > 0:
            if board != primary_board and board not in secondary_board:
                log.info(f"board is not primary and not in secondary list, board : {board} ")
                continue
        elif board != primary_board:
            log.info("board is not primary ")
            continue

        if company_id and mail_id:
            if company_id in company_to_mail_dict:
                if company_to_mail_dict[company_id]:
                    email_id_list = company_to_mail_dict[company_id]
                    email_id_list.append(mail_id)
                else:
                    company_to_mail_dict[company_id] = [mail_id]
            else:
                company_to_mail_dict[company_id] = [mail_id]
    return company_to_mail_dict, mail_id_to_board, mail_to_company_dict, message_list


def generate_outlook_email(request):
    """
    It will generate the Outlook email
    :param request:
    :return:
    """
    data = request.POST
    subject = data.get(OutlookEmail.subject.value, "")
    survey_url = data.get(OutlookEmail.survey_url.value, "")
    mail_body = data.get(OutlookEmail.email_body.value, "")

    excel_file = request.FILES["excel_file"]

    # you may put validations here to check extension or file size
    wb = pd.read_excel(excel_file)

    if len(subject.strip()) > 0 and len(mail_body.strip()) > 0:
        log.info("Both subject length and mail body length is not zero")
    else:
        log.info("Either subject length is zero or mail body length is zero")
        messages.error(request, "Please provide subject and mail body")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def create_message(email_recipient,
                   email_subject,
                   email_message, from_send,
                   attachment_location=[], toggle=False):

    to_address = ", ".join([email.strip() for email in email_recipient if "@gartner.com" not in email])
    msg = MIMEMultipart()
    msg['From'] = from_send.strip()
    msg["To"] = to_address
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_message, 'html', 'utf-8'))

    for f in attachment_location:
        part = MIMEApplication(f.read(), Name=f.name)
        part['Content-Disposition'] = 'attachment; filename="%s"' % (f.name)
        msg.attach(part)
    try:
        smtp = smtplib.SMTP('mailrelay.labgartner.com', 25)
        smtp.sendmail(from_send, to_address, msg.as_string())
        smtp.close()
    except Exception as e:
        log.error(f" SMPT server connection error  {e}")
        return False
    return True


def mail_sending(row, email_type=True):
    """
    It will send the email
    :param row:
    :return: None
    """
    email_body = create_email_body(row)
    if email_type:
        status = create_message(row["to_email"], row["subject"], email_body, row["from_send"],
                                attachment_location=row['files'],
                                toggle=False)
    else:

        status = send_email_api(row["to_email"], row["subject"], email_body, row["from_send"],
                                attachment_location=row['files'],
                                toggle=False)
    if status:
        log.info(f"***************** sending using smtp complete *****************")
        return f"Successful mail send to {row['to_email']}"
    else:
        return f"Error Sending mail send to {row['to_email']}"


def create_email_body(row):
    """
    Created email body
    :param row:
    :return:
    """
    df = pd.DataFrame(row["links"])
    df.fillna("", inplace=True)
    to_name = row['to_email'][0].split('.')[0]
    from_name = row['from_send'].split('.')[0]
    greetings = f"Hi {to_name.capitalize()}, \n\n"
    regards = f"<br>Thanks,<br>{from_name.capitalize()}"
    email_body = greetings + row["mail_content"] + df.to_html(index=False) + regards
    return email_body


def send_email_stmp(msg):
    """
    Email trigger through the smtp
    :param msg:
    :return:
    """
    try:
        server = smtplib.SMTP('mailrelay.labgartner.com', 25)
        server.ehlo()
        server.starttls()
        server.send_message(msg)
        log.info('email sent to successfully ')
        server.quit()
    except Exception as e:
        log.error(f" SMPT server connection error  {e}")
        return False
    return True


def send_email_api(email_recipient,
                   email_subject,
                   email_message, from_send,
                   attachment_location='', toggle=False):
    """
    It will create the email body as of the composer
    :param email_recipient: to address email list
    :param email_subject: subject of the email
    :param email_message: body of the message content
    :param from_send: send email
    :param attachment_location:  attachments if any
    :return
    """

    body = {
        'grant_type': 'authorization_code',
        'client_id': '6e79b0f1-e961-489d-97d2-9081343c8a87',
        'client_secret': 'Jnx8Q~iyKYVbeEOcdsJNoXXFo~_8K2usNZojVcUx',
        'scope': 'https://graph.microsoft.com/.default',
        'redirect_uri': 'http://localhost:8000/getAToken'
    }
    body[
        'code'] = "0.AScAmezfmOVmL0WHcYy3wF2hQvGweW5h6Z1Il9KQgTQ8iocnANA.AgABAAIAAAAtyolDObpQQ5VtlI4uGjEPAgDs_wUA9P_rjKYTrFw39OWBv-qK6lAZ1PWMzI8D-dp6k6JQkikaxNUu-szPOiTT7xLMtyEJIFqo3NoQGdG02rgyEJuMFNCeJPVWW7rDbnt7Y0v46_FJrvcZj9gbgxOZVEYH8vQA0uGYh_lD93drzaCBBFB28YBiqejmIV6KTwsf0QQ-sZjCZyFoZBxOOrNCNigLSnZveTNBaZe0KfBhRmu9NqanU9nSutFMk2KLR9hiQcRP0owTssqnTC1S94mzOb-Ta1D07D-gvcnJYCdcrthRPgerIZlufIUt4a5t1GfC-R5VUrrYVV5dU5O-vPoIu0cnVNDLdZejsTuSj2ITs2INSitjTe1xoxm5np0H5xcKAQw6hEAM_EjrO5odmBrKsMEJ_dGIePGU0dpJWmkg91h_7PTU-NGySbNneStjHy67yQadh720PevXibmJl8uSOqaltgc2Ko8dESpUB-6pdrbS5wpQe4ep91JECZgk5hOSFscl8BzK5EVkChYmgQOYBJbBq0szmC3haKZ6WnMKeSdzKnYTmWAyzzHvigisc2hEsarhgSi_uJHFnJjrKlIafPxQFWv3Kb76Ma_gXzxdtQXyHJ2YpT6WRw1Lu7jWQ5RuNTraSAWJ4JxzWQiwTi_XPAJeyehvGqDmNQlg3IpqICG6rWiQGniN8F5KTO16hbOq4zse0LZ4ZTOECoxSjDm-n-4WonFAoppKa5t2GVZmXmq6rz7qUAfN1NzaXsl6n8es-_hF12Tn27_NhAUWSx8_YV6rJ-wq1vpeBvqpRk9lIkNN5oOmwqpAwbCLl8REZhwFmoC_kk2tClIXi-tyKrJSqy1UL0yuZuMb1q3uwyspOnxOljjDFZ8"

    payload = {
        'grant_type': 'client_credentials',
        'client_id': '6e79b0f1-e961-489d-97d2-9081343c8a87',
        'client_secret': 'Jnx8Q~iyKYVbeEOcdsJNoXXFo~_8K2usNZojVcUx',
        'scope': 'https://graph.microsoft.com/.default'
    }
    try:
        response = Token(body)
        token = response.post()
    except Exception as e:
        log.error("Authorization code has expired due to inactivity")

    try:
        obj = MailSender("kunkusuresh.babu@labgartner.com", token=token)
        message = email_message
        to_address = [email.strip() for email in email_recipient if "@gartner.com" not in email]
        subject = email_subject
        obj.send_email(to_addresses=to_address, subject=subject, message_body=message,
                       attachment_paths=attachment_location)
        log.info('email sent to successfully ')
    except Exception as e:
        log.error(f" Graph API server connection error  {e}")
        return False
    return True
